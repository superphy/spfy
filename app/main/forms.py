from flask import current_app
from flask_wtf import Form
from wtforms import SelectField

from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class TaskForm(Form):
    task = SelectField('Task')

    validators = [
        FileRequired(message='There was no file!'),
        FileAllowed(['txt'], message='Must be a txt file!')
    ]

    input_file = FileField('', validators=validators)
    submit = SubmitField(label="Upload")

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.task.choices = [(task, task) for task in current_app.config['TASKS']]
