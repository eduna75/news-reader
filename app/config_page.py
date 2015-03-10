from flask import request, render_template, session, flash, redirect, url_for, g
from app.db_connect import DBConnect as DBc
from app import app, post_generator
from app.authenticate import login_required
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


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are logged out!')
    return redirect(url_for('index'))


@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    urls = [dict(id=row[0], url=row[1], name=row[2]) for row in g.db.execute('SELECT * FROM url').fetchall()]
    error = None
    return render_template('config.html', theme_list=g.theme_list[0], urls=urls, error=error, site_config=g.config)


@app.route('/run_post')
@login_required
def run_post():
    message = 'post generating finished with %s results' % post_generator.generator()
    flash(message)
    return redirect(url_for('config'))


"""Form handlers"""


@app.route('/news_config', methods=['GET', 'POST'])
def news_config():
    urls = [dict(id=row[0], url=row[1], name=row[2]) for row in g.db.execute('SELECT * FROM url').fetchall()]

    error = None
    if request.method == 'POST':
        if 'delete' in request.values:
            g.db.execute('DELETE FROM url WHERE url_id=?', request.form.values())
            g.db.commit()
            return redirect(url_for('config'))
        elif request.form['rssurl'] is None or '' and request.form['name'] is None or '':
            error = "you didn't fill in all the fields: "
        else:
            try:
                if request.form['active'] is 'on2':
                    rss_active = 0
                elif request.form['active'] is 'on1':
                    rss_active = 1
                else:
                    rss_active = 1
                form_input = [(request.form['rssurl']), (request.form['name']), rss_active]
                g.db.execute('INSERT INTO url(url, name, active) VALUES (?,?,?);', form_input)
                g.db.commit()
                return redirect(url_for('run_post'))
            except BaseException as e:
                print "That didn't go as planned! ", e
                error = "You didn't fill in all the fields or maybe a double entry:"
        return redirect(url_for('config'))

    return render_template('config.html', site_config=g.config, error=error, urls=urls)