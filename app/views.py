from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.login.models import User
from flask import render_template, request, url_for, redirect, session, flash, g
from app.db_connect import DBConnect as DBc
from os import walk
from werkzeug.security import check_password_hash, generate_password_hash


@app.before_request
def before_request():
    g.db = DBc.db_connect()
    g.config = DBc().con_config()
    g.user = None

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

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
    post = [dict(id=row[0], title=row[1], summary=row[2], link=row[3], source=row[10], time=row[4]) for row in
            g.db.execute('SELECT * FROM news INNER JOIN url ON source=url_id').fetchall()]

    urls = [dict(id=row[0], url=row[1], name=row[2]) for row in g.db.execute('SELECT * FROM url').fetchall()]

    # login part
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash(u'Welcome %r' % user.name)
            return redirect(url_for('backend.run_post'))
        flash(u'Wrong email or password')
    return render_template('index.html', post=post, length=len(post), urls=urls, theme_list=g.theme_list[0],
                           site_config=g.config, form=form, regform=g.regform, session=session, google_id=app.config[
            'GOOGLE_ID'])


@app.route('/help')
def help_page():
    return render_template('help.html', form=g.form, regform=g.regform, site_config=g.config,
                           theme_list=g.theme_list[0])


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegistrationForm(request.form)
    print regform.name.data
    print regform.email.data
    print regform.password.data
    try:
        if regform.is_submitted():
            print 'this'
            user = User(name=regform.name.data, email=regform.email.data,
                        password=generate_password_hash(regform.password.data))
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return redirect(url_for('index'))
    except BaseException as e:
        print e
    return render_template('register.html', form=g.form, regform=regform, theme_list=g.theme_list[0],
                           site_config=g.config)