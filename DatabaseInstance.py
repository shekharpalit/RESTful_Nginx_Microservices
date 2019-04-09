import sqlite3
from flask import Flask, request, jsonify, g, Response




app = Flask(__name__)
USER_DATABASE = './DataBase/users.db'
COMMENTS_DATABASE = './DataBase/comments.db'
TAGS_DATABASE = './DataBase/tags.db'
ARTICLE_DATABASE = './DataBase/article.db'
def get_userdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(USER_DATABASE)  #create a database instance and use it for later execution
        print("database instance is created")
    return db

def get_commentsdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(COMMENTS_DATABASE)  #create a database instance and use it for later execution
        print("database instance is created")
    return db

def get_tagsdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(TAGS_DATABASE)  #create a database instance and use it for later execution
        print("database instance is created")
    return db

def get_articledb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(ARTICLE_DATABASE)  #create a database instance and use it for later execution
        print("database instance is created")
    return db



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
