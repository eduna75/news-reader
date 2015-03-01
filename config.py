__author__ = 'justus'


# default config
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'N\xb3\x95\xcf\xc3\xd0\x8c2\x8a\xa73\xbc\x1c\xc8\xcd3&\xb6\xdf\xfa\xd1\xd0\x1d\xcc'


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False