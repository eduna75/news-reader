from os import walk
from flask import Blueprint, render_template, g, request, redirect, url_for, flash, session
from app.db_connect import DBConnect as DBc
from app.authenticate import login_required
from app import post_generator



node = Blueprint('backend', __name__, url_prefix='/backend')


@node.before_request
def before_request():
    g.db = DBc.db_connect()
    g.config = DBc().con_config()

    g.theme_list = []
    for root, dir_name, file_name in walk('./app/static/bootswatch'):
        g.theme_list.append(dir_name)


@node.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@node.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are logged out!')
    return redirect(url_for('index'))


@node.route('/')
def backend():
    urls = [dict(id=row[0], url=row[1], name=row[2]) for row in g.db.execute('SELECT * FROM url').fetchall()]
    active = []
    error = None
    return render_template('backend/config.html', theme_list=g.theme_list[0], urls=urls, error=error,
                           site_config=g.config)


@node.route('/run_post/')
@login_required
def run_post():
    message = 'post generating finished with %s results' % post_generator.generator()
    flash(message)
    return redirect(url_for('backend.backend'))


"""Form handlers"""


@node.route('/news_config/', methods=['GET', 'POST'])
def news_config():
    urls = [dict(id=row[0], url=row[1], name=row[2]) for row in g.db.execute('SELECT * FROM url').fetchall()]

    active = 'active in'
    rss_active = 1
    error = None
    if request.method == 'POST':
        if request.form['active'] is 'on2':
            rss_active = 0
        elif request.form['active'] is 'on1':
            rss_active = 1
        try:
            if request.form['rssurl'] is None or '' and request.form['name'] is None or '':
                error = "you didn't fill in all the fields: "
            else:
                form_input = [(request.form['rssurl']), (request.form['name']), rss_active]
                g.db.execute('INSERT INTO url(url, name, active) VALUES (?,?,?);', form_input)
                g.db.commit()
        except BaseException as e:
            print "That didn't go as planned! ", e
            error = "You didn't fill in all the fields or maybe a double entry:"
        return redirect(url_for('backend.backend'))

    return redirect(url_for('backend.backend'))


@node.route('/delete_feed/', methods=['GET', 'POST'])
def delete_feed():
    print request.form
    if request.method == 'POST':
        print request.values
        if 'delete' in request.values:
            g.db.execute('DELETE FROM url WHERE url_id=?', request.form.values())
            g.db.commit()
            flash('rss feed has been deleted')
            return redirect(url_for('backend.backend'))
    return redirect(url_for('backend.backend'))


@node.route('/set_template/', methods=['GET', 'POST'])
def set_template():
    if request.method == 'POST':
        print request.form['btn_theme']
        theme = request.form['btn_theme']
        g.db.execute('UPDATE config SET system_theme =?', (theme,))
        g.db.commit()
    return redirect(url_for('backend.backend', ))


@node.route('/main_config/', methods=['GET', 'POST'])
def main_config():
    if request.method == 'POST':
        data = [(request.form['site_name']), (request.form['slogan'])]
        print data
        g.db.execute('UPDATE config SET name_website = ?, slogan = ?', data)
        g.db.commit()
    return redirect(url_for('backend.backend'))