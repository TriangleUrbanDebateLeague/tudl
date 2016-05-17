from flask import Blueprint, current_app, request, render_template, flash, session, redirect, url_for, g
from modules.account.decorators import require_login, require_role, roles
from database import Volunteer, LoggedHours
from .forms import HoursEntryForm
from .reports import AllVolunteersReport

volunteer = Blueprint("volunteer", __name__, template_folder="templates", url_prefix="/volunteer")

@volunteer.route("/you/")
@require_login
def you():
    return render_template("profile.html", volunteer=g.user.volunteer, fake=False)

@volunteer.route("/all/")
@require_role(roles.hours_approver)
def all_volunteers():
    report = AllVolunteersReport()
    return render_template("volunteers.html", report=report)

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

@volunteer.route("/hours/edit/<int:id>/", methods=["GET", "POST"])
@require_login
def edit_hours(id):
    form = HoursEntryForm(request.form)
    obj = LoggedHours.get(id=id)

    if not form.validate_on_submit():
        form = HoursEntryForm(obj=obj)
        return render_template("log_hours.html", form=form, editing=True)

    form.populate_obj(obj)
    obj.approved = 0
    obj.modifier = g.user
    obj.save()

    return redirect(url_for("volunteer.your_hours"))

@volunteer.route("/hours/all/")
@require_role(roles.hours_approver)
def all_hours():
    return render_template("all_hours.html", hours=LoggedHours.select().order_by(LoggedHours.date.desc()))

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
            # 0 -> do nothing, 1 -> approve, -1 -> reject
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

@volunteer.route("/hours/rejected/", methods=["GET", "POST"])
@require_role(roles.hours_approver)
def rejected_hours():
    if request.method == "GET":
        rejected_hours = LoggedHours.select().where(LoggedHours.approved == -1).order_by(LoggedHours.date.desc())
        return render_template("rejected_hours.html", hours=rejected_hours)
    else:
        hours = [int(k[5:]) for k in request.form.keys() if k.startswith("state")]
        unrejected = False
        deleted = 0
        unrejected = 0
        for id in hours:
            result = int(request.form["state{}".format(id)])
            # 0 -> do nothing, 1 -> unreject, -1 -> delete forever

            entry = LoggedHours.get(LoggedHours.id == id)

            if result == 0:
                continue
            elif result == -1:
                entry.delete_instance()
                deleted += 1
            elif result == 1:
                entry.approved = 0
                entry.modifier = g.user
                entry.save()
                unrejected += 1
            else:
                raise Exception("Tried to perform an undefined action on a rejected hours entry -- this should never happen")

        rejected_hours = LoggedHours.select().where(LoggedHours.approved == -1).order_by(LoggedHours.date.desc())
        flash("{} entries modified ({} unrejected, {} deleted forever).".format(unrejected + deleted, unrejected, deleted), "info")
        return render_template("rejected_hours.html", hours=rejected_hours)
