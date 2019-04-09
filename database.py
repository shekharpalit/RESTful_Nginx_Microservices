import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('./article.db', timeout=10)
conn.execute('CREATE TABLE if not exists article (article_id INTEGER PRIMARY KEY NOT NULL, title TEXT, author INTEGER NOT NULL, content TEXT NOT NULL, is_active_article TEXT, date_created INTEGER, date_modified INTEGER, url TEXT)')
print("Successfully created article database")
conn.close()

conn = sqlite3.connect('./comments.db', timeout=10)
conn.execute('CREATE TABLE if not exists comments (comment_id INTEGER PRIMARY KEY, comment TEXT, article_id INTEGER, user_name INTEGER, timestamp INTEGER )')
print("Successfully created comments database")
conn.close()

conn = sqlite3.connect('./tags.db', timeout=10)
conn.execute('CREATE TABLE if not exists tags (tag_id INTEGER PRIMARY KEY NOT NULL, tag_name TEXT, article_id INTEGER)')
print("Successfully created comments database")
conn.close()

conn = sqlite3.connect('./users.db', timeout=10)
conn.execute('CREATE TABLE if not exists users (user_name TEXT PRIMARY KEY NOT NULL,  hashed_password TEXT NOT NULL, full_name TEXT NOT NULL, email_id TEXT NOT NULL,  date_created DATE NOT NULL, is_active INTEGER NOT NULL)')
print("Successfully created users database")
conn.close()
