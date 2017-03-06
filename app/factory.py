'''
this is the app factory
'''

from flask import Flask
from flask_bootstrap import Bootstrap
from . import config
from .main.views import bp as main
from flask_uploads import UploadSet, IMAGES, configure_uploads
from raven.contrib.flask import Sentry
sentry = Sentry(dsn='https://508d71e54ad84c9483320f051cc798ce:3efb1bc16af34fe8b3e5861382a83c9c@sentry.io/135389')

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('LOCAL_SETTINGS', silent=True)

    # add extensions to app
    Bootstrap(app)
    sentry.init_app(app)

    app.register_blueprint(main)

    return app
