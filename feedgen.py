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
    r = requests.get('http://localhost:5000/article')
    jsonResponse = r.json()
    #print(jsonResponse)
    listOfArticle = list()

    for i in jsonResponse:
        itemTobeAppended = Item(
        title = i[1],
        link = i[7],
        description = i[3],
        author = i[2])
        pubDate =i[5]
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



if __name__ == '__main__':
    app.run(debug=True, port=5001)
