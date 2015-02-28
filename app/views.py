__author__ = 'justus'

from app import app
from flask import render_template
from app.db_connect import DBConnect as DBc
from os import walk


@app.route('/', methods=['GET', 'POST'])
def index():
    theme_list = []
    for root, dir_name, file_name in walk('./app/static/bootswatch'):
        theme_list.append(dir_name)

    db = DBc.db_connect()
    select = db.execute('SELECT * FROM news INNER JOIN url ON source=url_id')
    post = [dict(id=row[0], title=row[1], summary=row[2], link=row[3], source=row[10], time=row[4]) for row in
            select.fetchall()]
    db.close()

    site = DBc()
    site_config = site.con_config()

    url_db = DBc.db_connect()
    select = url_db.execute('SELECT * FROM url')
    urls = [dict(id=row[0], url=row[1], name=row[2]) for row in select.fetchall()]
    url_db.close()
    return render_template('index.html', post=post, length=len(post), urls=urls, theme_list=theme_list[0],
                           site_config=site_config)


@app.route('/help')
def help_page():
    site = DBc()
    site_config = site.con_config()
    return render_template('help.html', site_config=site_config)
