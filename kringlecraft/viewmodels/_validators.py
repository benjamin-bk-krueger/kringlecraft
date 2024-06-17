import re

from wtforms.validators import ValidationError


# Custom validator for standard ASCII characters
def ascii_validator(form, field):
    if not re.search(r"^[A-Za-z0-9_.+-]+$", field.data):
        raise ValidationError('Please use only letters, numbers or the characters -_.')


# Custom validator for standard ASCII characters and additional space
def space_ascii_validator(form, field):
    if not re.search(r"^[A-Za-z0-9_.+ -]*$", field.data):
        raise ValidationError('Please use only letters, numbers or the characters -_.')


# Custom validator for extended ASCII characters
def full_ascii_validator(form, field):
    if not re.search(r"^[\S\n\r\t\v ]*$", field.data):
        raise ValidationError('Please use only ASCII letters and numbers.')


# Custom validator for integer numbers
def integer_validator(form, field):
    if not re.search(r"^[0-9]+$", field.data):
        raise ValidationError('Please use only numbers.')
