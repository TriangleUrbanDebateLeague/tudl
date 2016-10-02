from flask import Blueprint, render_template, make_response, current_app, flash, url_for, request, g, redirect
from jinja2 import TemplateNotFound
from collections import OrderedDict
from modules.security.localutils import has_permission
from .forms import ApplyStateForm, StateTextForm
from .models import State, StatePosition, Event, StateText
from utils import flash_errors, send_email
import os
import json

states = Blueprint("states", __name__, template_folder="templates", url_prefix="/states")

with open(os.path.dirname(os.path.realpath(__file__)) + '/states.json', 'r') as f:
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
        send_email(current_app.config["EMAIL_FROM"], 'benjamin.burstein@unifieddemocracy.org', 'State Director Application - {}'.format(current_app.config.get("APP_NAME", "Unified Democracy")), message)
        send_email(current_app.config["EMAIL_FROM"], 'victoria.bevard@unifieddemocracy.org', 'State Director Application - {}'.format(current_app.config.get("APP_NAME", "Unified Democracy")), message)
        flash("Application Successful", "success")
        return redirect(url_for("staticpages.show_staticpage", page="index"))

@states.route("/<state_code>/edit/", methods=["GET", "POST"])
def edit_state(state_code):
    state = State.get(State.code ** state_code)
    if not (state.director.account == g.user or has_permission(g.user, "states", "admin")):
        flash("Nope.", "error")
        return redirect(url_for("staticpages.show_staticpage", page="index"))

    form = StateTextForm()
    if not form.validate_on_submit():
        forms = [StateTextForm(obj=text) for text in state.texts]
        for form in forms: form.delete.data = False
        return render_template("states/edit.html", state=state, forms=forms, new=StateTextForm())

    if not form.id.data:
        StateText.create(state=state, title=form.title.data, text=form.text.data)
        return redirect(url_for("states.edit_state", state_code=state_code))

    text = StateText.get(StateText.id == form.id.data)
    if text.state != state:
        return redirect(url_for("states.edit_state", state_code=state_code))

    if form.delete.data:
        StateText.delete().where(StateText.id == form.id.data).execute()

    else:
        form.populate_obj(text)
        text.save()

    return redirect(url_for("states.edit_state", state_code=state_code))
