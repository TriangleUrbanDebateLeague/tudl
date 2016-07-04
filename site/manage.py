from flask.ext.script import Manager
from app import create_app
import database as db

manager = Manager(create_app)
manager.add_option('-e', '--environment', dest='environment', required=True)

@manager.shell
def shell_ctx():
    return dict(db=db)

@manager.command
def sync_volunteers():
    """Fix any Volunteers where local names differ from account names"""
    volunteers = db.Volunteer.select().where(db.Volunteer.account != None)
    print("Syncing {} volunteer(s)".format(volunteers.count()))
    for volunteer in volunteers:
        print(volunteer.full_name)
        volunteer.local_first_name = volunteer.account.first_name
        volunteer.local_last_name = volunteer.account.last_name
        volunteer.save()

@manager.command
def create_db():
    """Create tables in the database"""
    tables = [db.Account, db.Volunteer, db.LoggedHours, db.Donation]
    for table in tables:
        table.create_table()
        print("Created table for {}".format(table))

@manager.command
def migrate_add_dob():
    """Add the date of birth field to the accounts table"""
    from playhouse.migrate import *
    migrator = SqliteMigrator(db.database)
    migrate(
            migrator.add_column('account', 'dob', db.Account.dob)
    )

if __name__ == '__main__':
    manager.run()
