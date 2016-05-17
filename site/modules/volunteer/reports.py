from modules.reports import BaseReport
from database import Volunteer, Account, LoggedHours
from peewee import fn

class AllVolunteersReport(BaseReport):
    columns = [("Last name", "local_last_name"), ("First name", "local_first_name"), ("Approved hours", "total_hours")]
    def get_data(self):
        query = Volunteer \
                .select(Volunteer,
                        Account,
                        fn.Sum(LoggedHours.hours).alias('total_hours')) \
                .join(Account) \
                .join(LoggedHours) \
                .where(LoggedHours.approved == 1) \
                .group_by(Account)
        return list(query)
