from peewee import *
database = SqliteDatabase(None)

import bcrypt
from modules.volunteer import localconfig

class BaseModel(Model):
    class Meta:
        database = database

class Account(BaseModel):
    first_name = CharField(64, verbose_name="First name")
    last_name = CharField(64, verbose_name="Last name")

    street_address = CharField(128, verbose_name="Address")
    city = CharField(64, verbose_name="City")
    state = CharField(2, verbose_name="State code")
    postal_code = CharField(5, verbose_name="ZIP code")

    email = CharField(64, unique=True, verbose_name="Email address")
    email_confirm_key = CharField(64, null=True)
    email_confirmed = BooleanField(default=False, verbose_name="Email confirmed?")

    password = CharField(60)

    role = IntegerField(default=0, verbose_name="Role code")

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
        raise IntegrityError("Account with id {} already has an associated Volunteer, but attach_volunteer was called".format(self.id))

    @property
    def volunteer(self):
        q = self.volunteers
        if q.count() == 0:
            return None
        if q.count() > 1:
            raise IntegrityError("Account with id {} has multiple associated Volunteers -- this should never happen".format(self.id))
        return next(q.iterator())

    @property
    def full_name(self, alt=False):
        if alt:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return "{}, {}".format(self.last_name, self.first_name)

class Volunteer(BaseModel):
    account = ForeignKeyField(Account, related_name='volunteers', null=True)

    local_first_name = CharField(64, null=True, verbose_name="Volunteer first name")
    local_last_name = CharField(64, null=True, verbose_name="Volunteer last name")

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

    def total_hours(self, approved_only=True):
        if approved_only:
            hours = self.hours.select(fn.Sum(LoggedHours.hours)).where(LoggedHours.approved == 1).scalar()
        else:
            hours = self.hours.select(fn.Sum(LoggedHours.hours)).where(LoggedHours.approved != -1).scalar()
        return hours if hours else 0

    @property
    def full_name(self, alt=False):
        if alt:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return "{}, {}".format(self.last_name, self.first_name)

class LoggedHours(BaseModel):
    volunteer = ForeignKeyField(Volunteer, related_name='hours')

    date = DateField(verbose_name="Date")
    description = CharField(512, verbose_name="Description")
    category = IntegerField()
    hours = DecimalField(verbose_name="Hours")

    approved = IntegerField(default=0)
    modifier = ForeignKeyField(Account)

    @property
    def category_str(self):
        return localconfig.hours_types[self.category]

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
    amount = IntegerField(verbose_name="Amount")
    first_name = CharField(64, verbose_name="First name")
    last_name = CharField(64, verbose_name="Last name")
    street_address = CharField(128, verbose_name="Address")
    city = CharField(64, verbose_name="City")
    state = CharField(2, verbose_name="State code")
    postal_code = CharField(5, verbose_name="ZIP code")
    email = CharField(64, verbose_name="Email address")
    phone = CharField(20, verbose_name="Phone number")
    occupation = CharField(128, verbose_name="Occupation")
    employer = CharField(128, verbose_name="Employer")
    stripe_success = BooleanField(default=False, verbose_name="Charge successful")
