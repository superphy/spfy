from flask import current_app
from flask_wtf import Form
from wtforms import SelectField

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


class TaskForm(Form):
    task = SelectField('Task')

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.task.choices = [(task, task) for task in current_app.config['TASKS']]

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
