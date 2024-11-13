from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (BooleanField, StringField, SelectField)
from wtforms.validators import (Length)
from markupsafe import escape  # to safely escape form data

from kringlecraft.viewmodels.__validators import (space_ascii_validator)
from kringlecraft.data.summaries import Summary
from kringlecraft.data.solutions import Solution
from kringlecraft.data.invitations import Invitation

# Every form used both in the Flask/Jinja templates as well the main Python app is defined here.
# Not all fields have full validators as they are used in modal windows.


class SummaryForm(FlaskForm):
    visible = BooleanField('Visible in Report', default=True)

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
    visible = BooleanField('Solution visible', default=True)
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


class InvitationForm(FlaskForm):
    world = SelectField('Select World', choices=[(1, "none")], validate_choice=False)
    # objective = SelectField('Select Objective', choices=[(1, "none")], validate_choice=False)
    usage = StringField('Usage', validators=[Length(max=100), space_ascii_validator])

    @property
    def world_content(self):
        return str(escape(self.world.data))

    # @property
    # def objective_content(self):
    #     return str(escape(self.objective.data))

    @property
    def usage_content(self):
        return str(escape(self.usage.data))

    def __init__(self, invitation: Invitation = None):
        super().__init__()
        if invitation is not None:
            self.usage.default = invitation.usage

    def set_field_defaults(self):
        self.world.default = self.world_content
        # self.objective.default = self.objective_content
        self.usage.default = self.usage.data
