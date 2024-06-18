from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (StringField, PasswordField, BooleanField, TextAreaField, HiddenField)
from wtforms.validators import (InputRequired, Email, Length, EqualTo)
from markupsafe import escape  # to safely escape form data

from kringlecraft.viewmodels._validators import full_ascii_validator

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


class ContactForm(FlaskForm):
    contact_name = StringField('Name', validators=[InputRequired(), Length(min=5, max=40), full_ascii_validator])
    email = StringField('E-Mail', validators=[InputRequired(), Email()])
    message = TextAreaField('Message', validators=[Length(max=1024), full_ascii_validator])
    check_captcha = HiddenField(default='0')
    captcha = StringField('Captcha', validators=[InputRequired(), EqualTo('check_captcha',
                                                                          message='Captcha does not match')])

    def __init__(self, captcha: int = 10):
        super().__init__()
        self.check_captcha.default = captcha

    def set_captcha(self, captcha: int = 10):
        self.check_captcha.default = captcha

    def escape_fields(self):
        self.contact_name.data = escape(self.contact_name.data)
        self.email.data = escape(self.email.data)
        self.message.data = escape(self.message.data)

    def set_field_defaults(self):
        self.contact_name.default = escape(self.contact_name.data)
        self.email.default = escape(self.email.data)
        self.message.default = escape(self.message.data)
