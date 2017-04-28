'''
this is the app factory
'''

from flask import Flask
from flask_bootstrap import Bootstrap
import config
from routes.views import bp as spfy
from flask_recaptcha import ReCaptcha


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('LOCAL_SETTINGS', silent=True)

    # disable strict slashes
    # this makes routes defined without trailing / applicable to requests with or w/o the slashes
    # ex. @bp.route('/users') can be accessed via /users or /users/
    app.url_map.strict_slashes = False

    # add extensions to app
    Bootstrap(app)
    recaptcha = ReCaptcha()
    recaptcha.init_app(app)

    app.register_blueprint(spfy)

    return app
