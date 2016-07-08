from .localconfig import hours_types
from database import BaseModel
from modules.account.models import Account
from peewee import *

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
        return hours_types[self.category]

    @property
    def approved_str(self):
        if self.approved == -1:
            return "Rejected"
        if self.approved == 1:
            return "Approved"
        return "Unapproved"
