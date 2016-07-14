from .forms import ListSubscribeForm, ListConfirmSubscribeForm
from .localutils import send_confirm_email
from .models import ListEntry
from flask import Blueprint, current_app, request, render_template, redirect, url_for

email_list = Blueprint("email_list", __name__, template_folder="templates", url_prefix="/list")

@email_list.route("/susbcribe/", methods=["GET", "POST"])
def list_subscribe():
    form = ListSubscribeForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("list/subscribe.html", form=form)

    if not current_app.config["SEND_EMAIL"]:
        flash("The application is not configured to send emails.", "error")
        return render_template("list/subscribe.html", form=form)

    if ListEntry.select().where(ListEntry.email == form.email.data).count() > 0:
        flash("You're already subscribed to the mailing list!", "error")
        return render_template("list/subscribe.html", form=form)

    confirm_key = send_confirm_email(form.email.data)
    ListEntry.create(email=form.email.data, email_confirm_key=confirm_key,
                     email_confirmed=False)

    return redirect(url_for("email_list.thanks"))

@email_list.route("/thanks/")
def thanks():
    return render_template("list/thanks.html")

@email_list.route("/confirm/<key>/", methods=["GET", "POST"])
def confirm_email(key):
    pass
