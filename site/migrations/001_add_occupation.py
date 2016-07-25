from playhouse.migrate import *
from modules.donations.models import Donation

def run(db):
    migrator = SqliteMigrator(db)
    migrate(migrator.add_column('donation', 'occupation', Donation.occupation))
