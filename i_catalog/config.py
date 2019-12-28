# Configration module
#
# imports
from os import path
from time import time
from json import loads

from .fn import rand_str


# base
class Config(object):
    # App environment
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = rand_str()

    # FLASK_SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AUTH
    STATE = {
        'state': rand_str(),
        'exp': int(time()) + 5 * 60
    }

    # get secrets as parameters

    def __init__(self, secrets):
        # GOOGLE_AUTH
        gsecrets = secrets.get('google', False)
        if gsecrets:
            self.GOOGLE_LOGIN_CLIENT_ID = gsecrets['client_id']
            self.GOOGLE_LOGIN_ACC_DOMAINS = gsecrets['redirect_uris']
            self.GOOGLE_LOGIN_CLIENT_SECRET = gsecrets['client_secret']

        # FACEBOOK_AUTH
        fbsecrets = secrets.get('facebook', False)
        if fbsecrets:
            self.FACEBOOK_LOGIN_APP_ID = fbsecrets['app_id']
            self.FACEBOOK_LOGIN_APP_SECRET = fbsecrets['app_secret']


# production
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'


# developing
class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


# testing
class TestingConfig(Config):
    TESTING = True
