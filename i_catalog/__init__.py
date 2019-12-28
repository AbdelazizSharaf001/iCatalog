#!/usr/bin/env python3
#
# imports ------------------------------------------------
from os import path

from flask import (
    Flask,
    jsonify,
    Blueprint,
    render_template
)
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .fn import secrets_load
from .config import (
    ProductionConfig,
    DevelopmentConfig,
    TestingConfig
)


# Engines       -----------------------------------------------
# start DB engine
db = SQLAlchemy(session_options={'expire_on_commit': False})

# login manager ------------------------------------------
login_manager = LoginManager()


# flask app -----------------------------------------------
def create_app(config=None):
    # initialize
    app = Flask(__name__.split(':')[0], instance_relative_config=True)

    # config
    # get secrets for auth configration
    secrets = secrets_load('%s/secrets' % (app.name))

    try:
        # Development
        if config in ['dev', 'Development', 'DevelopmentConfig']:
            app.config.from_object(DevelopmentConfig(secrets))
        # Test
        elif config in ['test', 'testing', 'testingconfig']:
            app.config.from_object(TestingConfig(secrets))
        # production
        else:
            app.config.from_object(ProductionConfig(secrets))

    except Exception:
        if path.isfile('.config'):
            # on any problem load production config if config.py exists
            app.config.from_object(ProductionConfig(secrets))
        else:
            # stop the app if no config procided
            print('Where is the config!')
            exit()

    # database init
    db.init_app(app)
    # .crud imported here to prevent import cycle
    # ` due to db import in crud.py
    from .crud import fill_DB

    # login
    # set login view
    login_manager.login_view = 'auth.login'

    # session protection level
    #
    # 'basic'   (default)   - permanent session
    # 'strong'              - non-permanent session
    # 'None'                - disable
    #
    # login_manager.session_protection = "strong"

    # init login manager with flask app
    login_manager.init_app(app)

    # blueprints
    # these models imported here to prevent import cycle
    # ` due to db import in models.py
    # auth blueprint
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    # oAuth blueprint
    from .auth import oAuth as oAuth_bp
    app.register_blueprint(oAuth_bp, url_prefix='/oAuth')
    # main/CRUD blueprint
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    # API blueprint
    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # init testing route if not in production mode
    if app.config['DEBUG'] or app.config['TESTING']:
        # Test blueprint
        from .test import test as test_blueprint
        app.register_blueprint(test_blueprint)

    # DB head start
    @app.before_first_request
    @app.before_request
    def before_request():
        fill_DB(config)

    # return for the browser
    return app
