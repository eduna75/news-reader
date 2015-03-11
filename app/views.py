__author__ = 'justus'

from app import app
from flask import render_template, request, url_for, redirect, session, flash, g
from app.db_connect import DBConnect as DBc
from os import walk


@app.before_request
def before_request():
    g.db = DBc.db_connect()
    g.config = DBc().con_config()

    g.theme_list = []
    for root, dir_name, file_name in walk('./app/static/bootswatch'):
        g.theme_list.append(dir_name)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():

    post = [dict(id=row[0], title=row[1], summary=row[2], link=row[3], source=row[10], time=row[4]) for row in
            g.db.execute('SELECT * FROM news INNER JOIN url ON source=url_id').fetchall()]

    urls = [dict(id=row[0], url=row[1], name=row[2]) for row in g.db.execute('SELECT * FROM url').fetchall()]

    # login part
    error = None
    if request.method == 'POST':
        if request.form['email'] != 'admin' or request.form['password'] != 'admin':
            error = "You shall not pass!"
        else:
            session['logged_in'] = True
            flash('You are now logged in!')
            return redirect(url_for('config'))

    return render_template('index.html', post=post, length=len(post), urls=urls, theme_list=g.theme_list[0],
                           site_config=g.config, error=error, session=session, google_id=app.config['GOOGLE_ID'])


@app.route('/help')
def help_page():
    return render_template('help.html', site_config=g.config, theme_list=g.theme_list[0])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', theme_list=g.theme_list[0], site_config=g.config, e=e), 404


@app.errorhandler(400)
def page_not_found(e):
    return render_template('404.html', theme_list=g.theme_list[0], site_config=g.config, e=e), 400


@app.errorhandler(401)
def page_not_found(e):
    return render_template('404.html', theme_list=g.theme_list[0], site_config=g.config, e=e), 401


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html', theme_list=g.theme_list[0], site_config=g.config, e=e), 405