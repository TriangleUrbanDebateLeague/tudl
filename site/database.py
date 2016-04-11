from peewee import *
database = SqliteDatabase("tft.db")

import bcrypt

class BaseModel(Model):
    class Meta:
        database = database

class Account(BaseModel):
    first_name = CharField(64)
    last_name = CharField(64)
    state = CharField(2)
    email = CharField(64, unique=True)
    email_confirm_key = CharField(64, null=True)
    email_confirmed = BooleanField(default=False)
    two_factor_enabled = BooleanField(default=False)
    two_factor_key = CharField(16, null=True)
    password = CharField(60)
    role = IntegerField(default=0)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def validate_password(self, password):
        return bcrypt.hashpw(self.password, password.encode("utf-8")) == self.password

class PasswordReset(BaseModel):
    account = ForeignKeyField(Account, related_name='resets')
    key = CharField(128)
    created_at = DateTimeField()
    used = BooleanField(default=False)
