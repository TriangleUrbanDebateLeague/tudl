from flask_wtf import Form
from wtforms import validators
from wtforms import StringField, HiddenField, BooleanField
from wtforms.fields.html5 import EmailField

class DonateForm(Form):
    stripe_token = HiddenField(_name='stripeToken')

    first_name = StringField('First name', [validators.Required(), validators.Length(max=64)])
    last_name = StringField('Last name', [validators.Required(), validators.Length(max=64)])

    street_address = StringField('Street address', [validators.Required(), validators.Length(max=128)])
    city = StringField('City', [validators.Required(), validators.Length(max=64)])
    state = StringField('State', [validators.Required(), validators.Length(min=2, max=2)])
    postal_code = StringField('ZIP code', [validators.Required(), validators.Regexp(r'\d{5}')])

    email = EmailField('Email', [validators.Required(), validators.Email(), validators.Length(max=64)])
    phone = StringField('Phone', [validators.Required(), validators.Length(min=10, max=20)])

    occupation = StringField('Occupation', [validators.Required(), validators.Length(max=128)])
    employer = StringField('Employer', [validators.Required(), validators.Length(max=128)])

    certification_statement = BooleanField('I understand the statements above')
