from playhouse.migrate import *
from modules.donations.models import Donation

def migrate(db):
    migrator = SqliteMigrator(db)
    migrate(migrator.add_column('donation', 'employer', Donation.employer))
