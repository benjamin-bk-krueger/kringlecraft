from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (StringField, PasswordField)
from wtforms.validators import (InputRequired, Email, Length, EqualTo)
from markupsafe import escape  # to safely escape form data

from kringlecraft.viewmodels.__validators import space_ascii_validator

# Every form used both in the Flask/Jinja templates as well the main Python app is defined here.
# Not all fields have full validators as they are used in modal windows.


class AccountForm(FlaskForm):
    user_name = StringField('Name', validators=[InputRequired(), Length(min=5, max=40), space_ascii_validator])
    email = StringField('E-Mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20),
                                                     EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Password Verification', validators=[InputRequired(), Length(min=8, max=20)])

    @property
    def user_content(self):
        return str(escape(self.user_name.data))

    @property
    def email_content(self):
        return str(escape(self.email.data))

    @property
    def password_content(self):
        return str(self.password.data)

    def set_field_defaults(self):
        self.user_name.default = self.user_content
        self.email.default = self.email_content
        self.password.default = self.password_content
