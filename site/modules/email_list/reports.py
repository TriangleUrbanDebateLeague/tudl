from modules.email_list.models import ListEntry
from modules.reports import BaseReport
from peewee import fn

class ConfirmedEmailsReport(BaseReport):
    columns = [("Last name", "last_name"), ("First name", "first_name"), ("Email", "email")]
    name = "Confirmed emails"
    def get_data(self):
        return list(ListEntry.select().where(ListEntry.email_confirmed == True))
