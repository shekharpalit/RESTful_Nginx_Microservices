from flask import Flask, request
from flask import jsonify
import json
import sqlite3
import requests
import datetime
from rfeed import *

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
        date =i[5])
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

@app.route('/rssFullFeed',methods = ['GET'])
def getSingleArticleFeed():
    articleData = requests.get('http://localhost:5003/article')
    articleJsonResponse = articleData.json()
    tagsData = requests.get('http://localhost:5002/tagsgrouped')
    tagsJsonResponse = tagsData.json()
    listOfArticle = list()

    for i in articleJsonResponse:
        curr_index =i[0]
        #print(tagsJsonResponse[curr_index-1][1])
        itemTobeAppended = Item(
        title = i[1],
        link = i[7],
        description = i[3],
        author = i[2],
        categories= tagsJsonResponse[curr_index-1][1])
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

@app.route('/rssCommentfeed',methods = ['GET'])
def getTagsFeed():
    r = requests.get('http://localhost:5004/comments')
    jsonResponse = r.json()
    #print(jsonResponse)
    listOfArticle = list()

    # for i in jsonResponse:
    #     itemTobeAppended = Item(
    #     title = i[1],
    #     link = i[7],
    #     description = i[3],
    #     author = i[2])
    #     pubDate =i[5]
    #     listOfArticle.append(itemTobeAppended)

    feed = Feed(
    title = "RSS Feed",
    link = "http://localhost:5001/rssfeed",
    description = "The description of rss feeds",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = listOfArticle)
    resultXML = feed.rss()
    return resultXML, 200



if __name__ == '__main__':
    app.run(debug=True, port=5001)
