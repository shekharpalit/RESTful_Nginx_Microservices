from functools import wraps
from flask import Flask, request, jsonify, g, Response
import sqlite3
from passlib.apps import custom_app_context as pwd_context
from DatabaseInstance import get_userdb




def check_auth(username, password):#print("inside check_auth")
    cur = get_userdb().cursor().execute("SELECT user_name, hashed_password from users WHERE user_name=?", (username,))
    row = cur.fetchall()
    if row[0][0] == username and pwd_context.verify(password,row[0][1]):
        return True
    else:
        return False

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 403,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def decorated():
    try:
        uid = request.authorization["username"]
        pwd = request.authorization["password"]
        if not uid or not pwd or check_auth(uid, pwd) == False:
            return authenticate()
        else:
            return jsonify(message = "OK")
    except:
        return "Need authentication for this operation\n", 401
