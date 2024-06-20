from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (StringField, PasswordField, TextAreaField, BooleanField)
from wtforms.validators import (InputRequired, Email, Length, EqualTo)
from markupsafe import escape  # to safely escape form data

from kringlecraft.viewmodels.__validators import (space_ascii_validator, full_ascii_validator)
from kringlecraft.data.users import User

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


class MailForm(FlaskForm):
    email = StringField('E-Mail', validators=[InputRequired(), Email()])
    description = TextAreaField('Description', validators=[Length(max=1024), full_ascii_validator])
    notification = BooleanField('Send notifications', default=True)

    @property
    def email_content(self):
        return str(escape(self.email.data))

    @property
    def description_content(self):
        return str(escape(self.description.data))

    @property
    def notification_content(self):
        return bool(self.notification.data)

    def __init__(self, user: User = None):
        super().__init__()
        if user is not None:
            self.email.default = user.email
            self.description.default = user.description
            self.notification.default = user.notification

    def set_field_defaults(self):
        self.email.default = self.email_content
        self.description.default = self.description_content
        self.notification.default = self.notification_content


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20),
                                                     EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Password Verification', validators=[InputRequired(), Length(min=8, max=20)])

    @property
    def password_content(self):
        return str(self.password.data)


class DeletionForm(FlaskForm):
    pass
