from flask_wtf import Form
from wtforms import StringField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class ListSubscribeForm(Form):
    email = EmailField("Email address", [validators.Required(), validators.Length(max=64), validators.Email()])

class ListConfirmSubscribeForm(Form):
    first_name = StringField("First name", [validators.Required(), validators.Length(max=64)])
    last_name = StringField("Last name", [validators.Required(), validators.Length(max=64)])
