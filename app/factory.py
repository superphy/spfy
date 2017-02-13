'''
this is the app factory
'''

from flask import Flask
from . import config
from .extensions import bootstrap, redis
from .main.views import bp as main
from flask_uploads import UploadSet, IMAGES, configure_uploads

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('LOCAL_SETTINGS', silent=True)

    #Upload
    images = UploadSet('images', IMAGES)
    configure_uploads(app, images)

    # add extensions to app
    bootstrap.init_app(app)

    app.register_blueprint(main)

    return app
