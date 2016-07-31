from .forms import DonateForm
from .models import Donation
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for, flash
from utils import flash_errors, send_email
import stripe
import os
from collections import OrderedDict
import json
from datetime import datetime

donations = Blueprint("donations", __name__, template_folder="templates", url_prefix="/donate")

with open(os.path.dirname(os.path.realpath(__file__)) + '/states.json', 'r') as f:
    states = OrderedDict(sorted(json.loads(f.read()).items(), key=lambda k: k[0]))

@donations.context_processor
def make_key_available():
    return dict(key=current_app.config["STRIPE_KEY_PUBLIC"])


def send_receipt_email(donation):
    header_date = datetime.now().strftime("%x")
    body_date = datetime.now().strftime("%A %B %d, %Y")
    text = render_template("donations/receipt_email.html", donation=donation, header_date=header_date, body_date=body_date)
    send_email('benjamin.burstein@unifieddemocracy.org', donation.email, "Thanks for your donation to Unified Democracy!", text, "html")

@donations.route("/", methods=["GET", "POST"])
def donate():
    form = DonateForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("donations/donate.html", form=form, states=states)

    stripe.api_key = current_app.config["STRIPE_KEY_SECRET"]

    token = form.stripe_token.data
    amount = int(form.amount.data * 100)

    if(request.form.get('recurring') == "false"):
        recurring_donation = False
    else:
        recurring_donation = True

    try:
        donation = Donation.create(amount=amount, first_name=form.first_name.data, last_name=form.last_name.data,
                                   street_address=form.street_address.data, city=form.city.data, state=form.state.data,
                                   postal_code=form.postal_code.data, email=form.email.data, occupation=form.occupation.data, 
                                   employer=form.employer.data, recurring=recurring_donation, agreed=form.agreed.data)
        if not donation.recurring:
            stripe.Charge.create(amount=amount, receipt_email=form.email.data, currency="usd", source=token, description="Unified Democracy Donation #{}".format(donation.id))
        else:
            plan = stripe.Plan.create(id=donation.id, amount=amount, currency='USD', interval='month', name="Unified Democracy Recurring Donation #{} - {} {} ".format(donation.id, form.first_name.data, form.last_name.data))
            customer = stripe.Customer.create(email=form.email.data, source=token, description="Unified Democracy Recurring Donation #{} - {} {} ".format(donation.id, form.first_name.data, form.last_name.data), plan=plan.id)
        donation.stripe_success = True
        donation.save()
        send_receipt_email(donation)
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
