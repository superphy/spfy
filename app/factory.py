'''
this is the app factory
'''

from flask import Flask
from . import config
from .extensions import bootstrap, redis
from .main.blueprints import bp as main

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('LOCAL_SETTINGS', silent=True)

    # add extensions to app
    bootstrap.init_app(app)

    app.register_blueprint(main)

    return app
