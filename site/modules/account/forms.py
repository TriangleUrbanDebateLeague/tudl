from flask_wtf import Form
from wtforms import validators
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField

class AccountCreateForm(Form):
    first_name = StringField('First name', [validators.Required(), validators.Length(max=64)])
    last_name = StringField('Last name', [validators.Required(), validators.Length(max=64)])
    email = EmailField('Email', [validators.Required(), validators.Email(), validators.Length(max=64)])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=5, max=92),
                                          validators.EqualTo('confirm_password', message='Passwords must match!')])
    confirm = PasswordField('Confirm password')

class AccountLoginForm(Form):
    email = EmailField('Email', [validators.Required(), validators.Email(), validators.Length(max=64)])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=5, max=92)])

class AccountPasswordResetForm(Form):
    email = EmailField('Email', [validators.Required(), validators.Email()])
