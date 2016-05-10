from flask import Blueprint, current_app, request, render_template, flash, session, redirect, url_for
from modules.account.decorators import require_login
from database import Volunteer

volunteer = Blueprint("volunteer", __name__, template_folder="templates", url_prefix="/volunteer")

@volunteer.route("/you/")
@require_login
def you():
    return render_template("profile.html")
