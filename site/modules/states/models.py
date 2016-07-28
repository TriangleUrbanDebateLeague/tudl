from database import BaseModel
from modules.account.models import Account
from peewee import *

class State(BaseModel):
    code = CharField(2, verbose_name="State code", unique=True)
    name = CharField(32, verbose_name="State name", unique=True)

    @property
    def director(self):
        dir_ = self.positions.where(StatePosition.role == 99)
        if dir_.count() == 0:
            return None
        elif dir_.count() == 1:
            return dir_[0]
        else:
            raise IntegrityError("{} has more than 1 director".format(self.name.title()))
    

class Event(BaseModel):
    name = CharField(128, verbose_name="Event name")
    date = DateField(formats=["%Y", "%m/%Y", "%Y-%m-%d"], verbose_name="Date")
    state = ForeignKeyField(State, related_name="events")

class StatePosition(BaseModel):
    state = ForeignKeyField(State, related_name="positions")
    account = ForeignKeyField(Account, related_name="state_positions")
    title = CharField(64, verbose_name="Position title", null=True)
    bio = CharField(8192, verbose_name="Position biography", null=True)
    role = IntegerField(default=0, verbose_name="Role")
