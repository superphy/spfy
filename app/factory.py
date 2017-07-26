'''
this is the app factory
'''

from flask import Flask
from flask_bootstrap import Bootstrap
import config
from routes.views import bp as spfy
from routes.ra_views import bp_ra_views
from routes.ra_posts import bp_ra_posts
from routes.ra_statuses import bp_ra_statuses
from routes.ra_module_database import bp_ra_db
from routes.ra_module_metadata import bp_ra_meta
from flask_recaptcha import ReCaptcha
from flask_cors import CORS, cross_origin
from raven.contrib.flask import Sentry

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
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # sentry
    if hasattr(config, 'SENTRY_DSN'):
        sentry = Sentry(dsn=config.SENTRY_DSN)
        sentry.init_app(app)

    app.register_blueprint(spfy)
    # register the new blueprints used by reactapp
    app.register_blueprint(bp_ra_views)
    app.register_blueprint(bp_ra_posts)
    app.register_blueprint(bp_ra_statuses)
    app.register_blueprint(bp_ra_db)
    app.register_blueprint(bp_ra_meta)

    return app
