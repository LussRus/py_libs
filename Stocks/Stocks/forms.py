from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class change_param_setting(FlaskForm):
    top = StringField('Top')
    bottom = StringField('Bottom')
    submit = SubmitField()