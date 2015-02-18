__author__ = 'justus'

from app import app
from flask import render_template, request, redirect, url_for
import sqlite3


def db_connect():
    conn = sqlite3.connect('app/news-reader.db')
    return conn


@app.route('/')
def index():
    db = db_connect()
    select = db.execute('SELECT * FROM news')
    post = [dict(id=row[0], title=row[1], summary=row[2], link=row[3], time=row[4]) for row in select.fetchall()]
    db.close()
    return render_template('index.html', post=post, length=len(post))


@app.route('/config', methods=['GET', 'POST'])
def config():
    db = db_connect()
    select = db.execute('SELECT * FROM url')
    urls = [dict(id=row[0], url=row[1], name=row[2])for row in select.fetchall()]
    db.close()

    error = None
    if request.method == 'POST':
        if request.form['rssurl'] is None or request.form['name'] is None:
            error = "you didn't fill in all the fields: "
        else:
            try:
                form_input = [(request.form['rssurl']), (request.form['name'])]
                db_input = db_connect()
                db_input.execute('INSERT INTO url(url, name) VALUES (?,?);', form_input)
                db_input.commit()
                db_input.close()
                print request.form['rssurl'], request.form['name']
            except BaseException as e:
                print "That didn't go as planned! ", e
                error = "You didn't fill in all the fields or maybe a double entry:"
    return render_template('config.html', urls=urls, error=error)