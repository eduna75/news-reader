__author__ = 'justus'

from flask import request, render_template, session, flash, redirect, url_for
from flask.ext.login import LoginManager
from app.db_connect import DBConnect as DBc
from app import app
from functools import wraps
import os


login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'N\xb3\x95\xcf\xc3\xd0\x8c2\x8a\xa73\xbc\x1c\xc8\xcd3&\xb6\xdf\xfa\xd1\xd0\x1d\xcc'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('config_login'))
    return wrap


@app.route('/config_login', methods=['GET', 'POST'])
def config_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "You don't have the right to enter!"
        else:
            session['logged_in'] = True
            flash('You are now logged in!')
            return redirect(url_for('config'))
    return render_template('config_login.html', title='the login shit here!', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are logged out!')
    return redirect(url_for('index'))


@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    db = DBc.db_connect()
    select = db.execute('SELECT * FROM url')
    urls = [dict(id=row[0], url=row[1], name=row[2])for row in select.fetchall()]
    db.close()

    error = None
    if request.method == 'POST':
        if request.form['rssurl'] is None or request.form['name'] is None:
            error = "you didn't fill in all the fields: "
        else:
            try:
                if 1 in request.form.values():
                    active = 1
                else:
                    active = 0
                form_input = [(request.form['rssurl']), (request.form['name']), active]
                db_input = DBc.db_connect()
                db_input.execute('INSERT INTO url(url, name, active) VALUES (?,?,?);', form_input)
                db_input.commit()
                db_input.close()
                return redirect(url_for('run_post'))
            except BaseException as e:
                print "That didn't go as planned! ", e
                error = "You didn't fill in all the fields or maybe a double entry:"

    return render_template('config.html', urls=urls, error=error)


@app.route('/run_post')
@login_required
def run_post():
    os.system('app/post_generator.py')
    print 'finished'
    return redirect(url_for('config'))