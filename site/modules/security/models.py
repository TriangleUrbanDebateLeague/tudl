from database import BaseModel
from modules.account.models import Account
from peewee import *

class Permission(BaseModel):
    account = ForeignKeyField(Account, related_name="permissions")
    module = CharField(64)
    permission = CharField(64)
    data = CharField(256, null=True)
