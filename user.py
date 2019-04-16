from flask import Flask, request, jsonify, g, Response
from passlib.apps import custom_app_context as pwd_context
import sqlite3
import datetime
from passlib.apps import custom_app_context as pwd_context
from DatabaseInstance import get_userdb
from authentication import *
app = Flask(__name__)


#remaining handle sql query fail and return the status codes
#create user other
@app.route('/user', methods=['POST'])
def InsertUser():
    if request.method == 'POST':
        executionState:bool = False
        cur = get_userdb().cursor()
        data =request.get_json(force= True)
        try:
            date_created = datetime.datetime.now()
            is_active = 1
            hash_password = pwd_context.hash(data['hashed_password'])
            cur.execute( "INSERT INTO users ( user_name, hashed_password, full_name, email_id, date_created, is_active ) VALUES (:user_name, :hashed_password, :full_name, :email_id, :date_created, :is_active)",
            {"user_name":data['user_name'], "hashed_password":hash_password, "full_name":data['full_name'], "email_id":data['email_id'], "date_created":date_created,"is_active":is_active})
            if(cur.rowcount >=1):
                executionState = True
            get_userdb().commit()

        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data Instersted Sucessfully"), 201
            else:
                return jsonify(message="Failed to insert data"), 409

#update user

@app.route('/user', methods=['PATCH'])

def UpdateUser():
    if request.method == 'PATCH':
        executionState:bool = False
        cur = get_userdb().cursor()
        try:
            data  = request.get_json(force=True)
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            hash_password = pwd_context.hash(data['hashed_password'])
            cur.execute("UPDATE users SET hashed_password=? WHERE user_name=? AND EXISTS(SELECT 1 FROM users WHERE user_name=? AND is_active=1)", (hash_password, uid,uid))
            if(cur.rowcount >=1):
                executionState = True
                get_userdb().commit()
        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Updated SucessFully"), 201
            else:
                return jsonify(message="Failed to update the data"), 409


#delete user

@app.route('/user', methods=['DELETE'])

def DeleteUser():
    if request.method =="DELETE":
        executionState:bool = False
        cur = get_userdb().cursor()
        try:
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("UPDATE users SET is_active =? WHERE user_name=? AND EXISTS(SELECT 1 FROM users WHERE user_name=? AND is_active=1)", (0,uid,uid))

            if cur.rowcount >= 1:
                executionState = True
            get_userdb().commit()

        except sqlite3.Error as er:
            print(er)
            get_userdb().rollback()
             #save
        finally:
            if executionState:
                return jsonify(message="Data SucessFully deleted"), 200
            else:
                return jsonify(message="Failed to delete data"), 409




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


@app.route('/auth-server', methods= ['POST'])
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


if __name__== "__main__":
    app.run(debug=True)
