from playhouse.migrate import *
from modules.account.models import Account

def migrate(db):
    migrator = SqliteMigrator(db)
    migrate(migrator.add_column('account', 'dob', Account.dob))
