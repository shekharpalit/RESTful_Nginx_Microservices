from flask import Flask, request
from flask import jsonify
import json
import sqlite3
import requests
import datetime
from rfeed import *
import xml.dom.minidom

app = Flask(__name__)

@app.route('/rssfeed',methods = ['GET'])
def getFeed():
    r = requests.get('http://localhost:5003/article')
    jsonResponse = r.json()
    #print(jsonResponse)
    listOfArticle = list()
    #this is summary feed
    for i in jsonResponse:
        itemTobeAppended = Item(
        title = i[1],
        link = i[7],
        #description = i[3],
        author = i[2],
        pubDate =datetime.datetime.strptime(i[5], "%Y-%m-%d %H:%M:%S.%f"))
        listOfArticle.append(itemTobeAppended)

    feed = Feed(
    title = "RSS Feed",
    link = "http://localhost:5001/rssfeed",
    description = "The description of rss feeds",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = listOfArticle)
    resultXML = feed.rss()
    return resultXML, 200

@app.route('/rssfullfeed',methods = ['GET'])
def getSingleArticleFeed():
    articleData = requests.get('http://localhost:5003/article')
    articleJsonResponse = articleData.json()
    listOfArticle = list()

    for i in articleJsonResponse:
        curr_index =i[0]
        request_tag_url_string= "http://localhost:5002/tags/grouped/"+str(i[0])
        tagsData = requests.get(request_tag_url_string)
        tagsRecieved = tagsData.json()

        if None in tagsRecieved[0]:
            tagsAsCategories =""
        else:
            tagsAsCategories =tagsRecieved[0]

        request_comments_url_string= "http://localhost:5004/commentscount/"+str(i[0])
        commentCountData = requests.get(request_comments_url_string)
        commentCountRecieved = commentCountData.json()
        if None in commentCountRecieved[0]:
            commentsCount ="0"
        else:
            commentsCount = commentCountRecieved[0]

        itemTobeAppended = Item(
        title = i[1],
        link = i[7],
        description = i[3],
        author = i[2],
        categories =tagsAsCategories,
        comments =commentsCount)
        listOfArticle.append(itemTobeAppended)


    feed = Feed(
    title = "RSS Feed",
    link = "http://localhost:5001/rssfullfeed",
    description = "The description of rss feeds",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = listOfArticle)
    resultXML = feed.rss()
    return resultXML, 200

@app.route('/rsscommentfeed',methods = ['GET'])
def getTagsFeed():
    articleData = requests.get('http://localhost:5003/article')
    articleJsonResponse = articleData.json()
    listOfArticle = list()

    for i in articleJsonResponse:
        request_comments_url_string= "http://localhost:5004/commentsOfArticle/"+str(i[0])
        commentCountData = requests.get(request_comments_url_string)
        commentCountRecieved = commentCountData.json()
        if len(commentCountRecieved) is 0:
             comments ="0"
        else:
            comments = commentCountRecieved[0]

        itemTobeAppended = Item(
        title = i[1],
        link = i[7],
        description = i[3],
        author = i[2],
        comments=comments)
        listOfArticle.append(itemTobeAppended)

    feed = Feed(
    title = "RSS Feed",
    link = "http://localhost:5001/rssfeed",
    description = "The description of rss feeds",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = listOfArticle)
    resultXML = feed.rss()
    dom = xml.dom.minidom.parse(resultXML)
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)
    return resultXML, 200



if __name__ == '__main__':
    app.run(debug=True)
