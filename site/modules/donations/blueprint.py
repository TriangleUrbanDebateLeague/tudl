from .forms import DonateForm
from .models import Donation
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from utils import flash_errors
import stripe

donations = Blueprint("donations", __name__, template_folder="templates", url_prefix="/donate")

@donations.context_processor
def make_key_available():
    return dict(key=current_app.config["STRIPE_KEY_PUBLIC"])

@donations.route("/", methods=["GET", "POST"])
def donate():
    form = DonateForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("donations/donate.html", form=form)

    stripe.api_key = current_app.config["STRIPE_KEY_SECRET"]

    token = form.stripe_token.data
    amount = int(form.amount.data * 100)

    if(form.recurring.data == "false"):
        recurring_donation = False
    else:
        recurring_donation = True

    if amount > 25000:
        flash("You can't donate that much using this form!", "error")
        return redirect(url_for(".donate_failed"))

    try:
        donation = Donation.create(amount=amount, first_name=form.first_name.data, last_name=form.last_name.data,
                                   street_address=form.street_address.data, city=form.city.data, state=form.state.data,
                                   postal_code=form.postal_code.data, email=form.email.data, recurring=recurring_donation)
        if not donation.recurring:
            stripe.Charge.create(amount=amount, currency="usd", source=token, description="Teens for Teens donation id {}".format(donation.id))
        else:
            plan = stripe.Plan.create(id=donation.id, amount=amount, currency='USD', interval='month', name="Teens for Teens Recurring Donation - {} {} ".format(form.first_name.data, form.last_name.data))
            customer = stripe.Customer.create(email=form.email.data, source=token, description="Teens for Teens Recurring Donation - {} {} ".format(form.first_name.data, form.last_name.data), plan=plan.id)
        donation.stripe_success = True
        donation.save()
        return redirect(url_for(".thanks"))
    except stripe.error.CardError:
        flash("Your card was declined :(", "error")
        return redirect(url_for(".donate_failed"))

@donations.route("/failed/")
def donate_failed():
    return render_template("donations/donation_failed.html")

@donations.route("/thanks/")
def thanks():
    return render_template("donations/thanks.html")
