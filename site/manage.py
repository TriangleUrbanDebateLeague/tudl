from app import create_app
from email.mime.text import MIMEText
from flask_script import Manager
from modules.account.models import Account, PasswordReset
from modules.donations.models import Donation
from modules.email_list.models import ListEntry
from modules.security.models import Permission
from modules.states.models import State, Event, StatePosition
from modules.volunteer.models import Volunteer, LoggedHours
from peewee import IntegrityError
from subprocess import Popen, PIPE
import csv
import database as db
import importlib
import json
import os

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

        account = volunteer.account
        account.first_name = account.first_name.strip().title()
        account.last_name = account.last_name.strip().title()
        account.save()

        print(volunteer.full_name)
        volunteer.local_first_name = account.first_name
        volunteer.local_last_name = account.last_name
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
def import_directors(filename):
    """Import state directors"""
    with open(filename) as f:
        for state, bio, director, do_import in csv.reader(f):
            if not int(do_import):
                print("Not importing {}".format(state))
                continue
            firstname, lastname = director.split(" ", maxsplit=1)
            state = State.get(name=state)
            if state.director is not None:
                print("State {} already has a director {}".format(state.code, state.director.account.full_name))
                continue
            account = Account.get(first_name=firstname, last_name=lastname)
            StatePosition.create(state=state, account=account, title="State Director", bio=bio, role=99)
            print("Added {} as the director for {}".format(account.full_name, state.code))

@manager.command
def assign_permission(email, module, permission):
    """Assign a permission to a user"""
    account = Account.get(email=email)
    Permission.create(account=account, module=module, permission=permission)

@manager.command
def send_email(from_, to, subject, input_file):
    with open(input_file) as f:
        text = f.read()
    message = MIMEText(text)
    message["From"] = from_
    message["To"] = to
    message["Subject"] = subject
    process = Popen(["/usr/bin/sendmail", "-t", "-oi"], stdin=PIPE)
    process.communicate(message.as_string().encode())

if __name__ == '__main__':
    manager.run()
