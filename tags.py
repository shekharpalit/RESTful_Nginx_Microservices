from flask import Flask, request
from flask import jsonify
import json
import sqlite3
from datetime import datetime
from DatabaseInstance import get_tagsdb


app = Flask(__name__)


@app.route('/tags',methods = ['GET'])
def getArticlesFromTag():
    if request.method == 'GET':
        data = request.args.get('tag')
        cur = get_tagsdb().cursor()
        cur.execute("Select article_id from tags WHERE tag_name = :tag_name ", {"tag_name":data})
        articlesList = cur.fetchall()
        if len(articlesList) ==0:
            return "No articles containing the tags", 204
        else:
            #fetch the urls of articles with list of result of article_ids
            #cur.execute("Select url from article WHERE article_id IN :articles", {"articles":articlesList})
            #urlList = cur.fetchall()
            return jsonify(articlesList), 200

@app.route('/tagsgrouped',methods = ['GET'])
def getTagsgrouped():
    if request.method == 'GET':
        data = request.args.get('tag')
        cur = get_tagsdb().cursor()
        cur.execute("Select  article_id, group_concat(tag_name) as tag_name from tags group by article_id order by article_id",)
        row = cur.fetchall()
        return jsonify(row), 200

#get tags from the url utility
@app.route('/tags/<string:article_id>',methods = ['GET'])
def getTagsFromArticle(article_id):
    if request.method == 'GET':
        cur = get_tagsdb().cursor()
        cur.execute("SELECT tag_name from tags WHERE article_id= :article_id ", {"article_id":article_id})
        row = cur.fetchall()
        return jsonify(row), 200

#get tags from the url utility
@app.route('/tags/grouped/<string:article_id>',methods = ['GET'])
def getTagsFromArticleID(article_id):
    if request.method == 'GET':
        cur = get_tagsdb().cursor()
        cur.execute("SELECT group_concat(tag_name) as tag_name from tags WHERE article_id= :article_id ", {"article_id":article_id})
        row = cur.fetchall()
        return jsonify(row), 200

@app.route('/tags', methods = ['POST'])

def addTagstoArticle():
    if request.method == 'POST':
        data = request.get_json(force=True)
        executionState:bool = False
        cur = get_tagsdb().cursor()
        try:
            #check if tag exists or not
            #check if the article exists or not
                cur.execute("INSERT INTO tags(tag_name, article_id) VALUES (:tag_name, :article_id)",{"tag_name": data['tag_name'],"article_id": data['article_id']})
                if (cur.rowcount >=1):
                    executionState =True
                get_tagsdb().commit()
        except:
            get_tagsdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Tag inserted successfully \n"),201
            else:
                return jsonify(message="Failed to insert tag"),409


#adding a new and existing tag to the article
@app.route('/tags', methods = ['PUT'])

def addTagsToExistingArticle():
    if request.method == 'PUT':
        data = request.get_json(force=True)
        tags =data['tags']
        article_id =data['article_id']
        #return 204 if not found
        executionState:bool = False
        try:
            for tag in tags:
                    cur = get_tagsdb().cursor()
                    cur.execute("INSERT INTO tags(tag_name, article_id) VALUES( :tag_name, :article_id )",{"tag_name":tag, "article_id":article_id})

            if (cur.rowcount >=1):
                executionState =True
            get_tagsdb().commit()
        except:
            get_tagsdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Added Tags to an existing article"),201
            else:
                return jsonify(message="Failed to add tags to the article"),409



@app.route('/tags', methods = ['DELETE'])

def deleteTagFromArticle():
    if request.method == 'DELETE':
        data = request.get_json(force=True)
        #article_id = request.args.get('article_id')
        #print(tag_name+article_id)
        executionState:bool = False
        cur = get_tagsdb().cursor()
        try:
            cur.execute("DELETE from tags where article_id= :article_id and tag_name= :tag_name ",{"tag_name":data['tag_name'],"article_id":data['article_id']})
            #check for query result
            if (cur.rowcount >=1):
                executionState =True
                get_tagsdb().commit()
        except:
            get_tagsdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Deleted Tag SucessFully"),200
            else:
                return jsonify(message="Failed to delete tags from article"),409



if __name__ == '__main__':
    app.run(debug=True)
