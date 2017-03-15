'''
this is the app factory
'''

from flask import Flask
from flask_bootstrap import Bootstrap
from . import config
from .spfyroutes.views import bp as spfy
from flask_recaptcha import ReCaptcha


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('LOCAL_SETTINGS', silent=True)

    # add extensions to app
    Bootstrap(app)
    recaptcha = ReCaptcha()
    recaptcha.init_app(app)

    app.register_blueprint(spfy)

    return app
