from flask import Blueprint, render_template, make_response, request
from jinja2 import TemplateNotFound

from peewee import fn
from modules.volunteer.models import Volunteer, LoggedHours
from modules.states.models import State
from modules.email_list.forms import ListSubscribeForm

staticpages = Blueprint("staticpages", __name__, template_folder="templates", url_prefix="")

@staticpages.context_processor
def expose_models():
	return dict(Volunteer=Volunteer, LoggedHours=LoggedHours, State=State, fn=fn)

@staticpages.route("/", defaults={"page": "index"})
@staticpages.route("/<page>/")
def show_staticpage(page):
	try:
		form = ListSubscribeForm(request.form)
		return render_template("staticpages/{}.html".format(page), form=form)
	except TemplateNotFound:
		return make_response(render_template("not_found.html"), 404)

