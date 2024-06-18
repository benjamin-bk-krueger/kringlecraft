from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (StringField, PasswordField, BooleanField)
from wtforms.validators import (InputRequired, Email, Length)
from markupsafe import escape  # to safely escape form data

# Every form used both in the Flask/Jinja templates as well the main Python app is defined here.
# Not all fields have full validators as they are used in modal windows.


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    remember = BooleanField('Remember me', default=True)

    def escape_fields(self):
        self.email.data = escape(self.email.data)
        self.remember.data = escape(self.remember.data)

    def set_field_defaults(self):
        self.email.default = escape(self.email.data)
        self.remember.default = escape(self.remember.data)
