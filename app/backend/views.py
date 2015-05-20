from app import db
from os import walk
from app.models import User, Feed, Category, Country, Language
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
    page = 'backend/news_config.html'
    url = []
    all_feeds = Feed.query.all()
    feeds = Feed.query.join(User.urls).filter(User.id == g.user.id).all()
    for feed in feeds:
        url.append(feed)
    error = None
    return render_template('backend/config.html', feeds=url, all_feeds=all_feeds, error=error, page=page)


@node.route('/user-config/', methods=['GET', 'POST'])
def user_config():
    page = 'backend/user_config.html'
    users = User.query.all()

    if request.method == 'POST':
        if 'Delete' in request.form:
            user = User.query.filter_by(id=request.form['Delete']).first()
            db.session.delete(user)
            db.session.commit()
            flash("the user account is deleted!")
            return render_template('backend/config.html', page=page, users=users)
    return render_template('backend/config.html', page=page, users=users)


"""Form handlers"""


@node.route('/profile/', methods=["GET", "POST"])
def profile():
    page = 'backend/profile.html'
    # change user name and email, password not yet.
    # todo add change password and reset password option.
    if request.method == "POST":
        name = User.query.filter_by(id=g.user.id).first()
        name.nickname = request.form['Alias']
        name.email = request.form['Email']
        db.session.add(name)
        db.session.commit()
        flash("Your info has been updated!")

    # option for user to delete the account
    if 'Delete' in request.form:
        print request.form['Delete'], 'it is in here'
        remove = User.query.filter_by(id=g.user.id).first()
        db.session.delete(remove)
        db.session.commit()
        session.pop('user_id', None)
        return redirect(url_for('index'))
    return render_template('backend/config.html', page=page)


@node.route('/news-config/', methods=['GET', 'POST'])
def news_config():

    error = None
    if request.method == 'POST':
        print request.form
        try:
            if request.form['rssurl'] is None or '' and request.form['name'] is None or '':
                error = "you didn't fill in all the fields: "
            else:
                link = Feed(name=request.form['name'], url=request.form['rssurl'], category=request.form['category'],
                            country=request.form['country'], language=request.form['language'])
                db.session.add(link)
                db.session.commit()

        except BaseException as e:
            print "That didn't go as planned! ", e
            error = "You didn't fill in all the fields or maybe a double entry:"
        return redirect(url_for('backend.feed_config'))

    return redirect(url_for('backend.backend'))


@node.route('/select-feed/', methods=['GET', 'POST'])
def select_feed():
    if request.method == 'POST':
        user = User.query.filter_by(id=g.user.id).first()
        for id in request.form.itervalues():

            feed = Feed.query.filter_by(id=id).first()
            user.urls.append(feed)
            db.session.commit()

            flash('RSS feed [ %s ] has been added to your list.' % feed.name)

    return redirect(url_for('backend.news_config'))


@node.route('/delete-feed/', methods=['GET', 'POST'])
def delete_feed():
    if request.method == 'POST':
        if 'delete' in request.values:
            user = User.query.filter_by(id=g.user.id).first()
            feed = Feed.query.filter_by(id=request.form['delete']).first()
            user.urls.remove(feed)
            db.session.commit()

            flash('rss feed has been deleted')
            return redirect(url_for('backend.news_config'))
    return redirect(url_for('backend.news_config'))


# todo change the database on these methods
@node.route('/set-template/', methods=['GET', 'POST'])
def set_template():
    if request.method == 'POST':
        theme = request.form['btn_theme']
        g.db.execute('UPDATE config SET system_theme =?', (theme,))
        g.db.commit()
    return redirect(url_for('backend.news_config'))


@node.route('/site-config/', methods=['GET', 'POST'])
def site_config():
    page = 'backend/site_config.html'
    if request.method == 'POST':
        data = [(request.form['site_name']), (request.form['slogan'])]
        g.db.execute('UPDATE config SET name_website = ?, slogan = ?', data)
        g.db.commit()
    return render_template('backend/config.html', page=page)


@node.route('/feed-config/', methods=['GET', 'POST'])
def feed_config():
    page = 'backend/feed_config.html'
    all_feeds = Feed.query.all()
    category = Category.query.all()
    country = Country.query.all()
    language = Language.query.all()

    if request.method == 'POST':
        if 'Delete' in request.form:
            feed = Feed.query.filter_by(id=request.form['Delete']).first()
            db.session.delete(feed)
            db.session.commit()
            flash("the feed has been deleted!")
            return redirect(url_for('backend.feed_config'))
    return render_template('backend/config.html', page=page, all_feeds=all_feeds, category=category, country=country,
                           language=language)