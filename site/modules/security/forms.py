from flask_wtf import Form
from wtforms import StringField
from wtforms import validators

class UserSearchForm(Form):
    search = StringField("Search string (partial first name, partial last name, or complete email address)", [validators.Required()])
