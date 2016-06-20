from database import Volunteer, LoggedHours, Account, database
from datetime import date
import csv

database.init("/home/protected/tft.db")

def find_or_create_volunteer(first_name, last_name):
    query = Volunteer.select().where(Volunteer.local_last_name == last_name & Volunteer.local_first_name == first_name)
    if query.count() > 0:
        return next(query.iterator())

    return Volunteer.create(local_first_name=first_name, local_last_name=last_name)

f = open("hours.csv")
hours_listing = csv.reader(f)

modifier = Account.get(id=1)

for name, hours in hours_listing:
    split_name = name.split()
    first_name, last_name = split_name[0], split_name[-1]

    volunteer = find_or_create_volunteer(first_name, last_name)
    LoggedHours.create(volunteer=volunteer, date=date(year=2016, month=3, day=9),
                       description="Automatically backlogged hours", category=5,
                       hours=int(hours), approved=1, modifier=modifier)
    print("Backlogged hours for", volunteer.full_name)

f.close()
