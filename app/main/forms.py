from flask import current_app
from flask_wtf import Form
from wtforms import SelectField

from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(Form):
    input_file = FileField('', validators=[
        FileRequired(),
        FileAllowed(['fna, fsa_nt'])
    ])
    submit = SubmitField(label="Upload")
