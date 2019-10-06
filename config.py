__author__ = 'justus'
import os
_basedir = os.path.abspath(os.path.dirname(__file__))


# default config
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'N\xb3\x95\xcf\xc3\xd0\x8c2\x8a\xa73\xbc\x1c\xc8\xcd3&\xb6\xdf\xfa\xd1\xd0\x1d\xcc'
    GOOGLE_ID = 'UA-39697368-1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
    RECAPTCHA_PUBLIC_KEY = '6Lf29gUTAAAAAPO9uqkFVMB1bfdypl3pSt6DzAz8'
    RECAPTCHA_PRIVATE_KEY = '6Lf29gUTAAAAAFmwUgXO3an8J8BNyj9woPH-nLXf'
    PERMANENT_SESSION_LIFE = True


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'news-reader.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    DEBUG = False