__author__ = 'justus'

from app import app
from flask import render_template
import sqlite3


def db_connect():
    conn = sqlite3.connect('app/news-reader.db')
    return conn


@app.route('/')
def index():
    db = db_connect()
    select = db.execute('SELECT * FROM news')
    post = [dict(id=row[0], title=row[1], summary=row[2], link=row[3], time=row[4]) for row in select.fetchall()]
    return render_template('index.html', post=post, length=len(post))


@app.route('/config')
def config():
    return render_template('config.html')