from database import BaseModel
from modules import security
from peewee import *
import bcrypt

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

    dob = DateField(formats=["%Y-%m-%d", "%m/%d/%Y"], null=True)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def validate_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), self.password.encode("utf-8")) == self.password.encode("utf-8")

    def has_permission(self, module, permission):
        return security.localutils.has_permission(self, module, permission)

    @property
    def volunteer(self):
        q = self.volunteers
        if q.count() == 0:
            return None
        if q.count() > 1:
            raise IntegrityError("Account with id {} has multiple associated Volunteers -- this should never happen".format(self.id))
        return next(q.iterator())

    @property
    def full_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    @property
    def informal_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

class PasswordReset(BaseModel):
    account = ForeignKeyField(Account, related_name='resets')
    key = CharField(128)
    created_at = DateTimeField()
    used = BooleanField(default=False)
