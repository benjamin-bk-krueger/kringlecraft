from flask_wtf import FlaskForm  # integration with WTForms, data validation and CSRF protection
from wtforms import (StringField, TextAreaField, BooleanField, SelectField, IntegerRangeField)
from wtforms.validators import (InputRequired, Length, URL, NumberRange)
from markupsafe import escape  # to safely escape form data

from kringlecraft.viewmodels.__validators import (space_ascii_validator, full_ascii_validator)
from kringlecraft.data.worlds import World
from kringlecraft.data.rooms import Room
from kringlecraft.data.objectives import Objective

# Every form used both in the Flask/Jinja templates as well the main Python app is defined here.
# Not all fields have full validators as they are used in modal windows.

FILE_ALT_ENDING = "_2"
FILE_ALT_WARNING = "Name already exists. New name selected."


class WorldForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100), space_ascii_validator])
    description = TextAreaField('Description', validators=[Length(max=1024), full_ascii_validator])
    visible = BooleanField('Visible', default=True)
    url = StringField('URL', validators=[URL(), Length(max=256)])
    archived = BooleanField('Archived', default=False)

    @property
    def name_content(self):
        return str(escape(self.name.data))

    @property
    def description_content(self):
        return str(escape(self.description.data))

    @property
    def visible_content(self):
        return bool(self.visible.data)

    @property
    def url_content(self):
        return str(escape(self.url.data))

    @property
    def archived_content(self):
        return bool(self.archived.data)

    def __init__(self, world: World = None):
        super().__init__()
        if world is not None:
            self.name.default = world.name
            self.description.default = world.description
            self.visible.default = world.visible
            self.url.default = world.url
            self.archived.default = world.archived

    def set_field_defaults(self, rename: bool = False):
        self.name.default = self.name_content
        if rename:
            self.name.default = self.name_content + FILE_ALT_ENDING
            self.name.errors.append(FILE_ALT_WARNING)
        self.description.default = self.description_content
        self.visible.default = self.visible_content
        self.url.default = self.url_content
        self.archived.default = self.archived_content


class RoomForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100), space_ascii_validator])
    description = TextAreaField('Description', validators=[Length(max=1024), full_ascii_validator])
    world = SelectField('Select World', choices=[(1, "none")], validate_choice=False)

    @property
    def name_content(self):
        return str(escape(self.name.data))

    @property
    def description_content(self):
        return str(escape(self.description.data))

    @property
    def world_content(self):
        return str(escape(self.world.data))

    def __init__(self, room: Room = None):
        super().__init__()
        if room is not None:
            self.name.default = room.name
            self.description.default = room.description

    def set_field_defaults(self, rename: bool = False):
        self.name.default = self.name_content
        if rename:
            self.name.default = self.name_content + FILE_ALT_ENDING
            self.name.errors.append(FILE_ALT_WARNING)
        self.description.default = self.description_content
        self.world.default = self.world_content


class ObjectiveForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100), space_ascii_validator])
    description = TextAreaField('Description', validators=[Length(max=1024), full_ascii_validator])
    difficulty = IntegerRangeField('Difficulty', validators=[NumberRange(min=0, max=6)])
    visible = BooleanField('Visible', default=True)
    type = SelectField('Type', choices=[(1, "none")], validate_choice=False)
    room = SelectField('Select Room', choices=[(1, "none")], validate_choice=False)

    @property
    def name_content(self):
        return str(escape(self.name.data))

    @property
    def description_content(self):
        return str(escape(self.description.data))

    @property
    def difficulty_content(self):
        return int(self.difficulty.data)

    @property
    def visible_content(self):
        return bool(self.visible.data)

    @property
    def type_content(self):
        return int(self.type.data)

    @property
    def room_content(self):
        return str(escape(self.room.data))

    def __init__(self, objective: Objective = None):
        super().__init__()
        if objective is not None:
            self.name.default = objective.name
            self.description.default = objective.description
            self.difficulty.default = objective.difficulty
            self.visible.default = objective.visible
            self.type.default = objective.type

    def set_field_defaults(self, rename: bool = False):
        self.name.default = self.name_content
        if rename:
            self.name.default = self.name_content + FILE_ALT_ENDING
            self.name.errors.append(FILE_ALT_WARNING)
        self.description.default = self.description_content
        self.difficulty.default = self.difficulty.data
        self.visible.default = self.visible.data
        self.type.default = self.type.data
        self.room.default = self.room_content
