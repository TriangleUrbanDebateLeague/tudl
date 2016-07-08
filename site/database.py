from peewee import *
database = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = database
