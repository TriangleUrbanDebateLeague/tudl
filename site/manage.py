from app import create_app
from flask_script import Manager
import database as db
import importlib
import json
import os
from peewee import IntegrityError

from modules.account.models import Account, PasswordReset
from modules.donations.models import Donation
from modules.email_list.models import ListEntry
from modules.security.models import Permission
from modules.volunteer.models import Volunteer, LoggedHours
from modules.states.models import State, Event, StatePosition

manager = Manager(create_app)
manager.add_option('-e', '--environment', dest='environment', required=True)

@manager.shell
def shell_ctx():
    return dict(db=db)

@manager.command
def sync_volunteers():
    """Fix any Volunteers where local names differ from account names"""
    volunteers = Volunteer.select().where(Volunteer.account != None)
    print("Syncing {} volunteer(s)".format(volunteers.count()))
    for volunteer in volunteers:
        print(volunteer.full_name)
        volunteer.local_first_name = volunteer.account.first_name
        volunteer.local_last_name = volunteer.account.last_name
        volunteer.save()

@manager.command
def create_db():
    """Create tables in the database"""
    tables = [Account, PasswordReset, Donation, Permission, Volunteer, LoggedHours, ListEntry, State, Event, StatePosition]
    for table in tables:
        if table.table_exists():
            print("Table already exists for {}".format(table))
        else:
            table.create_table()
            print("Created table for {}".format(table))

@manager.command
def run_migration(migration):
    """Run a migration"""
    importlib.import_module("migrations.{}".format(migration)).run(db.database)

@manager.command
def create_states():
    """Import State objects"""
    with open(os.path.dirname(os.path.realpath(__file__)) + '/modules/states/states.json', 'r') as f:
        states_list = json.loads(f.read())

    for state, abbrev in states_list.items():
        try:
            s = State.create(name=state, code=abbrev)
            print("Created {} - {}".format(s.name, s))
        except IntegrityError:
            print("{} already exists".format(state))

@manager.command
def assign_permission(email, module, permission):
    """Assign a permission to a user"""
    account = Account.get(email=email)
    Permission.create(account=account, module=module, permission=permission)

if __name__ == '__main__':
    manager.run()
