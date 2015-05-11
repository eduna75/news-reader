from dateutil import parser
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.login.models import User, Feed
from app.post_generator import post
from flask import render_template, request, url_for, redirect, session, flash, g, send_from_directory
from app.db_connect import DBConnect as DBc
from os import walk
from werkzeug.security import check_password_hash, generate_password_hash

########################################
#
# datetimeformat is a filter for jinja2
#
#######################################


def datetimeformat(value):
    value = parser.parse(value)
    return value.strftime('%A, %d %B %Y')


app.jinja_env.filters['datetimeformat'] = datetimeformat


@app.before_request
def before_request():
    g.config = DBc().con_config()
    g.user = None
    g.name = None
    g.google_id = app.config['GOOGLE_ID']

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        g.name = g.user.nickname
        g.feed = Feed.query.join(User.urls).filter(User.id == g.user.id).all()

    if 'user_id' not in session:
        g.form = LoginForm(request.form)

    g.theme_list = []
    for root, dir_name, file_name in walk('./app/static/bootswatch'):
        g.theme_list.append(dir_name)

    g.regform = RegistrationForm(request.form)
    g.form = LoginForm(request.form)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect(url_for('news', news=g.feed[0].name))

    # login part

    if g.form.validate_on_submit():
        user = User.query.filter_by(email=g.form.email.data).first()
        if g.form['logged_in'].data is True:
            session.permanent = True
        if user and check_password_hash(user.password, g.form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(u'Wrong email or password')
    return render_template('index.html', session=session)


@app.route('/news/<news>')
def news(news=None):
    feeds = post(Feed.query.join(User.urls).filter(User.id == g.user.id).filter(
        Feed.name == news).all())  # These are the news posts

    for i in [i for i, x in enumerate(g.feed) if x.name == news]:
        if i + 1 >= len(g.feed):
            i = -1
    return render_template('index.html', feeds=feeds, feed=g.feed, session=session, news=g.feed[i + 1].name,
                           heading=news)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegistrationForm(request.form)
    try:
        if regform.is_submitted() and regform.validate_on_submit():
            user = User(nickname=regform.name.data, email=regform.email.data,
                        password=generate_password_hash(regform.password.data))
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return redirect(url_for('index'))
    except BaseException as e:
        print e
        flash('This email address is already registered, please login or use another email address')
        return redirect(url_for('index'))
    else:
        flash(regform.errors)
        return redirect(url_for('index'))
    return render_template('register.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404


@app.errorhandler(400)
def page_not_found(e):
    return render_template('404.html', e=e), 400


@app.errorhandler(401)
def page_not_found(e):
    return render_template('404.html', e=e), 401


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html', e=e), 405


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html', e=e), 500


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])
