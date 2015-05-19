from app import db
from app.login import constansts as USER
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    urls = db.relationship('Feed', secondary='urls', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, nickname, email, password=None):
        self.nickname = nickname
        self.email = email
        self.password = password

    def get_status(self):
        return USER.STATUS[self.status]

    def get_role(self):
        return USER.ROLE[self.role]

    def __repr__(self):
        return '<User %r>' % self.nickname

    rel = db.Table('urls',
                   db.Column('feed_id', db.Integer, db.ForeignKey('feed.id')),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                   )


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    country = db.Column(db.Integer, db.ForeignKey('country.id'))
    language = db.Column(db.Integer, db.ForeignKey('language.id'))

    def __init__(self, name, url, category, country, language):
        self.name = name
        self.url = url
        self.category = category
        self.country = country
        self.language = language

    def __repr__(self):
        return '<Feed %r %r>' % (self.name, self.url)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    url = db.Column(db.String, unique=True)
    pub_date = db.Column(db.DateTime)

    def __init__(self, name, url, pub_date=None):
        self.name = name
        self.url = url
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r %r>' % (self.name, self.url)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    feed = db.relationship('Feed', backref='cat', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    feed = db.relationship('Feed', backref='count', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Country %r>' % self.name


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    english = db.Column(db.String(120), unique=True)
    language = db.Column(db.String(8), unique=True)
    feed = db.relationship('Feed', backref='lang', lazy='dynamic')

    def __init__(self, title, english, language):
        self.title = title
        self.english = english
        self.language = language

    def __repr__(self):
        return '<Language %r %r %r>' % (self.title, self.english, self.language)