from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (BooleanField)

from kringlecraft.data.summaries import Summary

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
