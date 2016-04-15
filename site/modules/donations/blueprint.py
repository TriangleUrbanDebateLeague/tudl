from flask import Blueprint, render_template, request, current_app

from utils import flash_errors
from .forms import DonateForm

donations = Blueprint("donations", __name__, template_folder="templates", url_prefix="/donate")

@donations.context_processor
def make_key_available():
    return dict(key=current_app.config["STRIPE_KEY_PUBLIC"])

@donations.route("/", methods=["GET", "POST"])
def donate():
    form = DonateForm(request.form)
    flash_errors(form)

    if not form.validate_on_submit():
        return render_template("donate.html", form=form)

    return render_template("donate.html", form=form)
