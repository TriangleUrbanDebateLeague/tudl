from playhouse.migrate import *

def migrate(db):
    migrator = SqliteMigrator(db)
    migrate(migrator.add_column('account', 'dob', db.Account.dob))
