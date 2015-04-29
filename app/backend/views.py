from app import db
from os import walk
from app.login.models import User, Feed
from flask import Blueprint, render_template, g, request, redirect, url_for, flash, session
from app.db_connect import DBConnect as DBc


node = Blueprint('backend', __name__, url_prefix='/backend')


@node.before_request
def before_request():
    g.db = DBc.db_connect()
    g.config = DBc().con_config()
    g.user = None

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

    g.theme_list = []
    for root, dir_name, file_name in walk('./app/static/bootswatch'):
        g.theme_list.append(dir_name)


@node.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@node.route('/logout/')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@node.route('/')
def backend():
    url = []
    all_feeds = Feed.query.all()
    feeds = Feed.query.join(User.urls).filter(User.id == g.user.id).all()
    for feed in feeds:
        url.append(feed)
    error = None
    print url, all_feeds
    return render_template('backend/config.html', feeds=url, all_feeds=all_feeds, error=error, user=g.user)


"""Form handlers"""


@node.route('/news_config/', methods=['GET', 'POST'])
def news_config():

    error = None
    if request.method == 'POST':
        try:
            if request.form['rssurl'] is None or '' and request.form['name'] is None or '':
                error = "you didn't fill in all the fields: "
            else:
                link = Feed(request.form['name'], request.form['rssurl'])
                db.session.add(link)
                db.session.commit()

        except BaseException as e:
            print "That didn't go as planned! ", e
            error = "You didn't fill in all the fields or maybe a double entry:"
        return redirect(url_for('backend.backend'))

    return redirect(url_for('backend.backend'))


@node.route('/select_feed/', methods=['GET', 'POST'])
def select_feed():
    if request.method == 'POST':
        user = User.query.filter_by(id=g.user.id).first()
        for id in request.form.itervalues():

            feed = Feed.query.filter_by(id=id).first()
            user.urls.append(feed)
            db.session.commit()

            flash('RSS feed [ %s ] has been added to your list.' % feed.name)

    return redirect(url_for('backend.backend'))


@node.route('/delete_feed/', methods=['GET', 'POST'])
def delete_feed():
    if request.method == 'POST':
        print request
        if 'delete' in request.values:
            user = User.query.filter_by(id=g.user.id).first()
            feed = Feed.query.filter_by(id=request.form['delete']).first()
            user.urls.remove(feed)
            db.session.commit()

            flash('rss feed has been deleted')
            return redirect(url_for('backend.backend'))
    return redirect(url_for('backend.backend'))


@node.route('/set_template/', methods=['GET', 'POST'])
def set_template():
    if request.method == 'POST':
        theme = request.form['btn_theme']
        g.db.execute('UPDATE config SET system_theme =?', (theme,))
        g.db.commit()
    return redirect(url_for('backend.backend'))


@node.route('/main_config/', methods=['GET', 'POST'])
def main_config():
    if request.method == 'POST':
        data = [(request.form['site_name']), (request.form['slogan'])]
        g.db.execute('UPDATE config SET name_website = ?, slogan = ?', data)
        g.db.commit()
    return redirect(url_for('backend.backend'))