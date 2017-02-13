from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class UploadForm(Form):
    input_file = FileField('', validators=[
        FileRequired()
    ])
    submit = SubmitField(label="Run")
