import os

SECRET_KEY = 'is-that-daisy'
REDIS_URL = '0.0.0.0/6379'
QUEUES = ['high','medium','low','default']
BOOTSTRAP_SERVE_LOCAL = True
MAX_TIME_TO_WAIT = 10

UPLOAD_FOLDER = 'app/tmp'
ALLOWED_EXTENSIONS = ['fna']
RECAPTCHA_ENABLED = True
RECAPTCHA_SITE_KEY = "6LfLNRgUAAAAAAMzTNg3dAE5YhW904EbJpTt4gm_"
RECAPTCHA_SECRET_KEY = ""
