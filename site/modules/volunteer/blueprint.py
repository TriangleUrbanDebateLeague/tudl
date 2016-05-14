from flask import Blueprint, current_app, request, render_template, flash, session, redirect, url_for, g
from modules.account.decorators import require_login, require_role, roles
from database import Volunteer, LoggedHours
from .forms import HoursEntryForm

volunteer = Blueprint("volunteer", __name__, template_folder="templates", url_prefix="/volunteer")

@volunteer.route("/you/")
@require_login
def you():
    return render_template("profile.html", volunteer=g.user.volunteer, fake=False)

@volunteer.route("/hours/")
@require_login
def your_hours():
    hours = g.user.volunteer.hours.order_by(LoggedHours.date.desc())
    return render_template("your_hours.html", hours=hours)

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

@volunteer.route("/hours/approve/", methods=["GET", "POST"])
@require_role(roles.hours_approver)
def approve_hours():
    if request.method == "GET":
        unapproved_hours = LoggedHours.select().where(LoggedHours.approved == 0).order_by(LoggedHours.date.desc())
        return render_template("unapproved_hours.html", hours=unapproved_hours)
    else:
        hours = [int(k[5:]) for k in request.form.keys() if k.startswith("state")]
        approved = 0
        denied = 0
        for id in hours:
            result = int(request.form["state{}".format(id)])
            if result == 0:
                continue
            elif result == 1:
                approved += 1
            elif result == -1:
                denied += 1
            else:
                raise Exception("Tried to set an hour's approved state to an invalid value -- this should never happen")

            entry = LoggedHours.get(LoggedHours.id == id)
            entry.approved = result
            entry.modifier = g.user
            entry.save()

        unapproved_hours = LoggedHours.select().where(LoggedHours.approved == 0).order_by(LoggedHours.date.desc())
        flash("{} entries modified ({} approved, {} rejected).".format(approved + denied, approved, denied), "info")
        return render_template("unapproved_hours.html", hours=unapproved_hours)
