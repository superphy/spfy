'''
this is the app factory
'''

from flask import Flask
from . import config
from .extensions import bootstrap, redis
from .blueprints import bp as main

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    # add extensions to app
    bootstrap.init_app(app)
    redis.init_app(app)

    app.register_blueprint(main)

    return app
