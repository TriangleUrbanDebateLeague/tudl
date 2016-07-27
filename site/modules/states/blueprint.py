from flask import Blueprint, render_template, make_response, current_app, flash, url_for, request
from jinja2 import TemplateNotFound
from collections import OrderedDict
from .forms import ApplyStateForm
from .models import State, StatePosition, Event
from utils import flash_errors, send_email
import os
import json

states = Blueprint("states", __name__, template_folder="templates", url_prefix="/states")

with open(os.path.dirname(os.path.realpath(__file__)) + '/templates/states/states.json', 'r') as f:
    states_list = OrderedDict(sorted(json.loads(f.read()).items(), key=lambda k: k[0]))

@states.route("/")
def main_state_page():
	return render_template("states/states.html", states=states_list)

@states.route("/<state_code>/", methods=["GET", "POST"])
def show_state_page(state_code):
    try:
        state = State.get(State.code ** state_code)
        positions = state.positions.order_by(StatePosition.role.desc())[1:]
        events = state.events.order_by(Event.date.desc())
        return render_template("states/state_base.html", state=state, positions=positions, events=events)
    except State.DoesNotExist:
    	form = ApplyStateForm(request.form)
    	if not form.validate_on_submit():
    		flash_errors(form)
    		return render_template("states/apply.html", form=form)
    	message = render_template("states/apply_email.html", form=form)
    	send_email('noreply@unifieddemocracy.org', 'benjamin.burstein@unifieddemocracy.org', 'State Director Application - {}'.format(current_app.config.get("APP_NAME", "Unified Democracy")), message)
    	flash("Application Successful", "success")
    	return redirect(url_for("staticpages.show_staticpage", page="index"))
