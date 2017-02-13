import os

SECRET_KEY = 'can-you-keep-a-secret'
REDIS_URL = 'redis://redis:6379/0'
QUEUES = ['high,medium,low,default']
BOOTSTRAP_SERVE_LOCAL = True
TASKS = ['Short task', 'Long task', 'Task raises error']
MAX_TIME_TO_WAIT = 10
