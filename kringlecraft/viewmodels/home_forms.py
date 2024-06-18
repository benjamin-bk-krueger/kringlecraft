from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (StringField, PasswordField, BooleanField, TextAreaField, HiddenField)
from wtforms.validators import (InputRequired, Email, Length, EqualTo)
from markupsafe import escape  # to safely escape form data

from kringlecraft.viewmodels.__validators import full_ascii_validator

# Every form used both in the Flask/Jinja templates as well the main Python app is defined here.
# Not all fields have full validators as they are used in modal windows.


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    remember = BooleanField('Remember me', default=True)

    @property
    def email_content(self):
        return str(escape(self.email.data))

    @property
    def password_content(self):
        return str(self.password.data)

    @property
    def remember_content(self):
        return bool(self.remember.data)

    def set_field_defaults(self):
        self.email.default = self.email_content
        self.remember.default = self.remember_content


class ContactForm(FlaskForm):
    contact_name = StringField('Name', validators=[InputRequired(), Length(min=5, max=40), full_ascii_validator])
    email = StringField('E-Mail', validators=[InputRequired(), Email()])
    message = TextAreaField('Message', validators=[Length(max=1024), full_ascii_validator])
    check_captcha = HiddenField(default='0')
    captcha = StringField('Captcha', validators=[InputRequired(), EqualTo('check_captcha',
                                                                          message='Captcha does not match')])

    @property
    def contact_content(self):
        return str(escape(self.contact_name.data))

    @property
    def email_content(self):
        return str(escape(self.email.data))

    @property
    def message_content(self):
        return str(escape(self.message.data))

    @property
    def captcha_content(self):
        return str(escape(self.captcha.data))

    def __init__(self, captcha: int = 10):
        super().__init__()
        self.check_captcha.default = captcha

    def set_captcha(self, captcha: int = 10):
        self.check_captcha.default = captcha

    def set_field_defaults(self):
        self.contact_name.default = self.contact_content
        self.email.default = self.email_content
        self.message.default = self.message_content


class PasswordForm(FlaskForm):
    email = StringField('E-Mail', validators=[InputRequired(), Email()])

    @property
    def email_content(self):
        return str(escape(self.email.data))

    def set_field_defaults(self):
        self.email.default = self.email_content


class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20),
                                                     EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Password Verification', validators=[InputRequired(), Length(min=8, max=20)])

    @property
    def password_content(self):
        return str(self.password.data)
