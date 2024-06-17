from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, PasswordField, BooleanField, HiddenField, FileField, TextAreaField, SelectField,
                     IntegerRangeField)
from wtforms.validators import ValidationError, InputRequired, EqualTo, Email, Length, URL, NumberRange


# Every form used both in the Flask/Jinja templates as well the main Python app is defined here.
# Not all fields have full validators as they are used in modal windows.

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    remember = BooleanField('Remember me', default=True)
