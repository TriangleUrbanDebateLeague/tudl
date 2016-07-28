from modules.states.models import *
import os
from collections import OrderedDict
import json
from database import database

database.init("tft.db")

with open(os.path.dirname(os.path.realpath(__file__)) + '/modules/states/templates/states/states.json', 'r') as f:
    states_list = OrderedDict(sorted(json.loads(f.read()).items(), key=lambda k: k[0]))

for state, abbrev in states_list.items():
	try:
		s = State.create(name=state, code=abbrev)
		print("Created {} - {}".format(s.name, s))
	except IntegrityError:
		print("{} already exists".format(state))