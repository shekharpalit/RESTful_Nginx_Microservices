from flask import Flask, request
from flask import jsonify
import json
from datetime import datetime
from DatabaseInstance import get_commentsdb

app = Flask(__name__)

@app.route('/commentscount/<string:article_id>',methods = ['GET'])
def getCommentcount(article_id):
    if request.method == 'GET':
        cur = get_commentsdb().cursor()
        cur.execute("Select  count(comment) as comment from comments where article_id= :article_id",{"article_id":article_id})
        row = cur.fetchall()
        return jsonify(row), 200

@app.route('/commentsOfArticle/<string:article_id>',methods = ['GET'])
def getCommentofEachArticle(article_id):
    if request.method == 'GET':
        cur = get_commentsdb().cursor()
        cur.execute("Select  group_concat(comment) from comments where article_id= :article_id group by article_id order by comment_id desc limit 10",{"article_id":article_id})
        row = cur.fetchall()
        return jsonify(row), 200


#Add comments to the database
@app.route('/comment', methods = ['POST'])
def AddComment():
    if request.method == 'POST':
        executionState:bool = False
        cur = get_commentsdb().cursor()
        data = request.get_json(force=True)
        try:
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            time_created = datetime.now()
            cur.execute("INSERT INTO comments (comment, user_name, article_id, timestamp) VALUES (:comment, :user_name,:article_id, :timestamp) ",{"comment":data['comment'], "user_name":uid, "article_id":data['article_id'], "timestamp": time_created})
            if (cur.rowcount >= 1):
                executionState = True
                get_commentsdb().commit()
        except:
            get_commentsdb().rollback()   #if it fails to execute rollback the database
            executionState = False
        finally:
            if executionState:
                return jsonify(message="Passed"), 201
            else:
                return jsonify(message="Fail"), 409    #use 409 if value exists and send the message of conflict

#delete a comment from the database
@app.route('/comment', methods = ['DELETE'])
def deleteComment():
    if request.method == 'DELETE':
        executionState:bool = False
        cur = get_commentsdb().cursor()
        try:
            data = request.args.get('comment_id')
            cur.execute("SELECT user_name FROM comments WHERE comment_id="+data)
            row = cur.fetchall()
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            if row[0][0] == uid:
                cur.execute("DELETE from comments WHERE user_name=? AND comment_id=?",(uid,data))
                if (cur.rowcount >= 1):
                    executionState = True
                get_commentsdb().commit()
        except:
            get_commentsdb().rollback()                  #if it fails to execute rollback the database
            executionState = False
        finally:
            if executionState:
                return jsonify(message="Passed"), 201
            else:
                return jsonify(message="Fail"), 409

#retrive all or n number of comments from the database
@app.route('/comment', methods = ['GET'])
def retriveComments():
    if request.method == 'GET':
        executionState:bool = False
        cur = get_commentsdb().cursor()
        try: #move the try block after the below for test case if the data is none or not then only try db connection
            data = request.args.get('article_id')
            data1 = request.args.get('number')
            executionState = True

            if data is not None and data1 is not None:
                cur.execute("SELECT timestamp, comment FROM(SELECT * FROM comments WHERE article_id="+data+" ORDER BY timestamp DESC LIMIT :data1)",{"data1":data1})
                retriveNcomments = cur.fetchall()
                get_commentsdb().commit()
                if list(retriveNcomments) == []:
                    return "No such value exists\n", 204
                return jsonify(retriveNcomments), 200

            if data is not None and data1 is None:
                cur.execute("SELECT comment from comments WHERE article_id="+data)
                retriveAllComments = cur.fetchall()
                get_commentsdb().commit()
                if list(retriveAllComments) == []:
                    return "No such value exists\n", 204
                return jsonify(len(retriveAllComments)), 200
        except:
            get_commentsdb().rollback() #if it fails to execute rollback the database
            executionState = False

        finally:
            if executionState == False:
                return jsonify(message="Fail"), 204

#Update the comments in the database for a particular user
@app.route('/comment', methods =['PUT'])
def UpdateComments():
    if request.method == 'PUT':
        executionState:bool = False
        cur = get_commentsdb().cursor()
        try:
            data = request.get_json(force = True)
            cur.execute("SELECT user_name FROM comments WHERE comment_id=?",(data['comment_id']))
            row = cur.fetchall()
            timeCreated = datetime.now()
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            if row[0][0] == uid:
                cur.execute("UPDATE comments set comment = ?,timestamp=? where user_name =? AND comment_id =?",  (data['comment'],timeCreated, uid, data['comment_id']))
                if (cur.rowcount >= 1):
                    executionState = True
                get_commentsdb().commit()
        except:
            get_commentsdb().rollback() #if it fails to execute rollback the database
            executionState = False

        finally:
            if executionState:
                return jsonify(message="Passed"), 201
            else:
                return jsonify(message="Fail"), 409

if __name__ == '__main__':
    app.run(debug=True, port=5004)
