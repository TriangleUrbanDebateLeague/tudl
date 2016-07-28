from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.fields.html5 import EmailField

class ApplyStateForm(Form):
	first_name = StringField('First Name', [validators.Required()])
	last_name = StringField('Last Name', [validators.Required()])
	email = EmailField('Email', [validators.Required(), validators.Email()])
	state = StringField('State', [validators.Required()])