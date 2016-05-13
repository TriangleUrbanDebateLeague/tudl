from peewee import *
database = SqliteDatabase(None)

import bcrypt
from modules.volunteer import localconfig

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

    @property
    def volunteer(self):
        q = self.volunteers
        if not q.count():
            return None
        return next(q.iterator())

class Volunteer(BaseModel):
    account = ForeignKeyField(Account, related_name='volunteers', null=True)

    local_first_name = CharField(64, null=True)
    local_last_name = CharField(64, null=True)

    @property
    def first_name(self):
        if self.account is not None:
            return self.account.first_name
        return self.local_first_name

    @property
    def last_name(self):
        if self.account is not None:
            return self.account.last_name
        return self.local_last_name

class LoggedHours(BaseModel):
    volunteer = ForeignKeyField(Volunteer, related_name='hours')

    date = DateField()
    description = CharField(512)
    category = IntegerField()
    hours = DecimalField()

    approved = IntegerField(default=0)
    modifier = ForeignKeyField(Account)

    @property
    def category_str(self):
        return hours_types[self.category]

    @property
    def approved_str(self):
        if self.approved == -1:
            return "Rejected"
        if self.approved == 1:
            return "Approved"
        return "Unapproved"

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
