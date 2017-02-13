from flask import current_app
from flask_wtf import Form
from wtforms import SelectField


class TaskForm(Form):
    task = SelectField('Task')

    def __init__(self, *args, **kwargs):
        super(Taskform, self).__init__(TaskForm, *args, **kwargs)
        self.task.choices = [(task, task) for task in current_app.config['TASKS']]
