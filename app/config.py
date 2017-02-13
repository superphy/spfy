import os

SECRET_KEY = 'can-you-keep-a-secret'
REDIS_URL = '0.0.0.0/6379'
QUEUES = ['high,medium,low,default']
BOOTSTRAP_SERVE_LOCAL = True
TASKS = ['Short task', 'Long task', 'Task raises error']
MAX_TIME_TO_WAIT = 10

# Uploads
UPLOADS_DEFAULT_DEST = TOP_LEVEL_DIR + '/app/uploads/'
UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/uploads/'
