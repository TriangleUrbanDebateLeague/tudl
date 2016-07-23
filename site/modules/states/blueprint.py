from flask import Blueprint, render_template, make_response
from jinja2 import TemplateNotFound
import os
import json
from collections import OrderedDict

states = Blueprint("states", __name__, template_folder="templates", url_prefix="/state")


with open(os.path.dirname(os.path.realpath(__file__)) + '/templates/states/states.json', 'r') as f:
    states_list = OrderedDict(sorted(json.loads(f.read()).items(), key=lambda k: k[1]))

@states.route("/")
def main_state_page():
	return render_template("states/states.html", states=states_list)

@states.route("/<state_code>/")
def show_state_page(state_code):
    state = state_code.upper()
    try:
        state_name = states_list[state].lower()
        return render_template("states/{}.html".format(state_name))
    except (KeyError, TemplateNotFound):
        return make_response(render_template("not_found.html"), 404)
