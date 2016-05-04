from peewee import *
database = SqliteDatabase(None)

import bcrypt

class BaseModel(Model):
    class Meta:
        database = database

class Account(BaseModel):
    first_name = CharField(64)
    last_name = CharField(64)

    street_address = CharField(128)
    city = CharField(64)
    state = CharField(2)
    postal_code = CharField(5)

    email = CharField(64, unique=True)
    email_confirm_key = CharField(64, null=True)
    email_confirmed = BooleanField(default=False)

    password = CharField(60)

    role = IntegerField(default=0)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def validate_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), self.password.encode("utf-8")) == self.password.encode("utf-8")

class PasswordReset(BaseModel):
    account = ForeignKeyField(Account, related_name='resets')
    key = CharField(128)
    created_at = DateTimeField()
    used = BooleanField(default=False)

class Donation(BaseModel):
    amount = IntegerField()
    first_name = CharField(64)
    last_name = CharField(64)
    street_address = CharField(128)
    city = CharField(64)
    state = CharField(2)
    postal_code = CharField(5)
    email = CharField(64)
    phone = CharField(20)
    occupation = CharField(128)
    employer = CharField(128)
    stripe_success = BooleanField(default=False)
