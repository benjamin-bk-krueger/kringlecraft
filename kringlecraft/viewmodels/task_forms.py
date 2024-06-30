from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (BooleanField, StringField)
from wtforms.validators import (Length)
from markupsafe import escape  # to safely escape form data

from kringlecraft.viewmodels.__validators import (space_ascii_validator)
from kringlecraft.data.summaries import Summary
from kringlecraft.data.solutions import Solution

# Every form used both in the Flask/Jinja templates as well the main Python app is defined here.
# Not all fields have full validators as they are used in modal windows.


class SummaryForm(FlaskForm):
    visible = BooleanField('Visible', default=True)

    @property
    def visible_content(self):
        return bool(self.visible.data)

    def __init__(self, summary: Summary = None):
        super().__init__()
        if summary is not None:
            self.visible.default = summary.visible

    def set_field_defaults(self):
        self.visible.default = self.visible.data


class SolutionForm(FlaskForm):
    visible = BooleanField('Visible', default=True)
    completed = BooleanField('Completed', default=True)
    ctf_flag = StringField('CTF Flag', validators=[Length(max=100), space_ascii_validator])

    @property
    def visible_content(self):
        return bool(self.visible.data)

    @property
    def completed_content(self):
        return bool(self.completed.data)

    @property
    def ctf_flag_content(self):
        return str(escape(self.ctf_flag.data))

    def __init__(self, solution: Solution = None):
        super().__init__()
        if solution is not None:
            self.visible.default = solution.visible
            self.completed.default = solution.completed
            self.ctf_flag.default = solution.ctf_flag

    def set_field_defaults(self):
        self.visible.default = self.visible.data
        self.completed.default = self.completed.data
        self.ctf_flag.default = self.ctf_flag.data
