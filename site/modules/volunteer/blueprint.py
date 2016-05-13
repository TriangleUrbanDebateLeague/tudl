from flask import Blueprint, current_app, request, render_template, flash, session, redirect, url_for, g
from modules.account.decorators import require_login, require_role, roles
from database import Volunteer, LoggedHours
from .forms import HoursEntryForm

volunteer = Blueprint("volunteer", __name__, template_folder="templates", url_prefix="/volunteer")

@volunteer.route("/you/")
@require_login
def you():
    return render_template("profile.html")

@volunteer.route("/hours/")
@require_login
def your_hours():
    return render_template("your_hours.html", hours=g.user.volunteer.hours)

@volunteer.route("/hours/log/", methods=["GET", "POST"])
@require_login
def log_hours():
    form = HoursEntryForm(request.form)

    if not form.validate_on_submit():
        return render_template("log_hours.html", form=form)

    LoggedHours.create(volunteer=g.user.volunteer, date=form.date.data,
                       description=form.description.data, category=form.category.data,
                       hours=form.hours.data, modifier=g.user)

    flash("Your hours have been entered and should be approved shortly.", "info")
    return redirect(url_for("volunteer.your_hours"))

@volunteer.route("/hours/approve/")
@require_role(roles.hours_approver)
def approve_hours():
    unapproved_hours = LoggedHours.select().where(LoggedHours.approved == 0)
    return render_template("unapproved_hours.html", hours=unapproved_hours)
