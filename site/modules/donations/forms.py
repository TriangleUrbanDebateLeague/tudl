from flask_wtf import Form
from wtforms import StringField, HiddenField, BooleanField, RadioField, DecimalField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class DonateForm(Form):
    stripe_token = HiddenField(_name='stripe_token')
    amount = DecimalField('Amount', [validators.Required(), validators.NumberRange(1.00, 250.00)])

    first_name = StringField('First name', [validators.Required(), validators.Length(max=64)])
    last_name = StringField('Last name', [validators.Required(), validators.Length(max=64)])

    street_address = StringField('Street address', [validators.Required(), validators.Length(max=128)])
    city = StringField('City', [validators.Required(), validators.Length(max=64)])
    state = StringField('State', [validators.Required(), validators.Length(min=2, max=2)])
    postal_code = StringField('ZIP code', [validators.Required(), validators.Regexp(r'\d{5}')])

    email = EmailField('Email', [validators.Required(), validators.Email(), validators.Length(max=64)])

    recurring = BooleanField('Recurring donation')
