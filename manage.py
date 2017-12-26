import redis
from flask_script import Server, Manager
from rq import Connection, Worker
from app.factory import create_app

# manager.add_command(
#     'runserver',
#     Server(host='0.0.0.0', port=5000, use_debugger=True, use_reloader=True))

from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app
from app.commands import InitDbCommand

# Setup Flask-Script with command line commands
manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command('init_db', InitDbCommand)

@manager.command
def runworker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()

if __name__ == '__main__':
    manager.run()
