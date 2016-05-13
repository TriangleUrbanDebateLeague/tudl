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

    def attach_volunteer(self):
        if self.volunteer is None:
            query = Volunteer.select().where(Volunteer.account == None & Volunteer.local_first_name == self.first_name & Volunteer.local_last_name == self.last_name)
            if query.count() == 1:
                volunteer = next(query.iterator())
                volunteer.account = self
                volunteer.save()
                return volunteer
            else:
                return Volunteer.create(account=self)
        raise IntegrityError("Account already has an associated Volunteer")

    @property
    def volunteer(self):
        q = self.volunteers
        if q.count() == 0:
            return None
        if q.count() > 1:
            raise IntegrityError("Account has multiple associated Volunteers -- this should never happen")
        return next(q.iterator())

    @property
    def full_name(self, alt=False):
        if alt:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return "{}, {}".format(self.last_name, self.first_name)

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
