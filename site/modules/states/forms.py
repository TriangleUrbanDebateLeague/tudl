from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField, validators
from wtforms.widgets import HiddenInput, TextArea
from wtforms.fields.html5 import EmailField

class ApplyStateForm(Form):
    first_name = StringField('First Name', [validators.Required()])
    last_name = StringField('Last Name', [validators.Required()])
    email = EmailField('Email', [validators.Required(), validators.Email()])
    state = StringField('State', [validators.Required()])

class StateTextForm(Form):
    id = IntegerField('ID', [validators.Optional()], widget=HiddenInput())
    title = StringField('Title', [validators.Required()])
    text = StringField('Text', [validators.Required()], widget=TextArea())
    delete = BooleanField("Delete", [validators.Optional()])
