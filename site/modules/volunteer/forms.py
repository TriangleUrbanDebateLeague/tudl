from .localconfig import hours_types
from flask_wtf import Form
from wtforms import StringField, DecimalField, SelectField, DateField
from wtforms import validators

def hours_type_list():
    return [(idx, val) for idx, val in enumerate(hours_types)]

class HoursEntryForm(Form):
    date = DateField('Date', [validators.Required()])
    hours = DecimalField('Hours', [validators.Required()])
    description = StringField('Activity description', [validators.Required(), validators.Length(max=512)])
    category = SelectField('Activity type', coerce=int, choices=hours_type_list())
