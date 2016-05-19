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

if __name__ == '__main__':
    manager.run()
