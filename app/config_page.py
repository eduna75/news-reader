__author__ = 'justus'

from flask import request, render_template, session, flash, redirect, url_for
from flask.ext.login import LoginManager
from app.db_connect import DBConnect as DBc
from app import app
from app.authenticate import login_required
import os


login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/config_login', methods=['GET', 'POST'])
def config_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "You shall not pass!"
        else:
            session['logged_in'] = True
            flash('You are now logged in!')
            return redirect(url_for('config'))
    site = DBc()
    site_config = site.con_config()
    return render_template('config_login.html', title='the login shit here!', error=error, site_config=site_config)


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

    site = DBc()
    site_config = site.con_config()

    error = None
    if request.method == 'POST':
        if 'delete' in request.values:
            db_delete = DBc.db_connect()
            db_delete.execute('DELETE FROM url WHERE url_id=?', request.form.values())
            db_delete.commit()
            db_delete.close()
            return redirect(url_for('config'))
        elif request.form['rssurl'] is None or '' and request.form['name'] is None or '':
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

    return render_template('config.html', urls=urls, error=error, site_config=site_config)


@app.route('/run_post')
@login_required
def run_post():
    os.system('app/post_generator.py')
    print 'finished'
    return redirect(url_for('config'))