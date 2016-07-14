from database import BaseModel
from peewee import *

class ListEntry(BaseModel):
    first_name = CharField(64, verbose_name="First name", null=True)
    last_name = CharField(64, verbose_name="Last name", null=True)

    email = CharField(64, unique=True, verbose_name="Email address")
    email_confirm_key = CharField(64)
    email_confirmed = BooleanField(default=False)
