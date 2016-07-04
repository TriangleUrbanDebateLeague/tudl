from flask import Blueprint, current_app, request, render_template, flash, session, redirect, url_for, g

from utils import flash_errors
from .localutils import send_confirm_email, send_reset_email, get_current_user
from .decorators import require_login
from .forms import AccountCreateForm, AccountLoginForm, AccountPasswordResetForm, AccountPasswordSetForm, AccountDobSetForm
from database import Account, PasswordReset
from datetime import datetime, timedelta

account = Blueprint("account", __name__, template_folder="templates", url_prefix="/account")

@account.route("/create/", methods=["GET", "POST"])
def create_account():
    form = AccountCreateForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("create.html", form=form)

    matching_accounts = Account.select().where(Account.email == form.email.data)
    if matching_accounts.count() > 0:
        flash("An account already exists with that email address.", "error")
        return render_template("create.html", form=form)

    if current_app.config['SEND_EMAIL']:
        email_confirmed = False
        email_confirm_key = send_confirm_email(form.first_name.data, form.email.data)
        flash("Account created. Please confirm your email; you should receive information on how to do this shortly.", "info")
    else:
        email_confirmed = True
        email_confirm_key = None
        flash("Account created.", "info")

    password = Account.hash_password(form.password.data)

    account = Account.create(first_name=form.first_name.data, last_name=form.last_name.data,
                             street_address=form.street_address.data, city=form.city.data,
                             state=form.state.data, postal_code=form.postal_code.data,
                             email=form.email.data, email_confirm_key=email_confirm_key,
                             email_confirmed=email_confirmed, password=password, dob=form.dob.data)

    account.attach_volunteer()

    return redirect(url_for('account.login'))

@account.route("/confirm_email/<key>/")
def confirm_email(key):
    matching_accounts = Account.select().where(Account.email_confirmed == False, Account.email_confirm_key == key)

    if matching_accounts.count() != 1:
        flash("Incorrect data.", "error")
    else:
        account = next(matching_accounts.iterator())
        account.email_confirmed = True
        account.save()
        flash("Email confirmed.", "success")

    return redirect(url_for('account.login'))

@account.route("/reset/", methods=["GET", "POST"])
def request_reset():
    form = AccountPasswordResetForm()

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("request_reset.html", form=form)

    try:
        account = Account.get(email=form.email.data)
        send_reset_email(account)
        flash("Password reset link sent.", "info")
    except Account.DoesNotExist:
        flash("No account was found with that email address.", "error")

    return render_template("request_reset.html", form=form)

@account.route("/reset/<key>/", methods=["GET", "POST"])
def reset_password(key):
    form = AccountPasswordSetForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("reset.html", form=form)

    try:
        reset = PasswordReset.get(key=key)
    except PasswordReset.DoesNotExist:
        flash("Invalid password reset key.", "error")
        return redirect(url_for("account.request_reset"))

    if reset.used:
        flash("Password reset key already used.", "error")
        return redirect(url_for("account.request_reset"))

    if reset.created_at - datetime.now() > timedelta(seconds=3600):
        flash("Password reset expired.", "error")
        return redirect(url_for("account.request_reset"))

    reset.account.password = Account.hash_password(form.password.data)
    reset.account.save()

    reset.used = True
    reset.save()

    flash("Password set.", "info")
    return redirect(url_for("account.login"))

@account.route("/login/", methods=["GET", "POST"])
def login():
    form = AccountLoginForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("login.html", form=form)

    matching_accounts = Account.select().where(Account.email == form.email.data)
    if matching_accounts.count() == 1:
        account = next(matching_accounts.iterator())
        if account.validate_password(form.password.data):
            if account.dob is not None:
                session["uid"] = account.id
                session["logged_in"] = True
                return redirect(request.args.get('next', url_for('account.info')))
            else:
                session["dob_uid"] = account.id
                return redirect(url_for("account.set_dob"))

    flash("Login failed.", "error")
    return render_template("login.html", form=form)

@account.route("/set_dob/", methods=["GET", "POST"])
def set_dob():
    if "dob_uid" not in session:
        return redirect(url_for("account.login"))

    form = AccountDobSetForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("dob.html", form=form)

    account = Account.get(id=session["dob_uid"])
    account.dob = form.dob.data
    account.save()

    session["uid"] = session.pop("dob_uid")
    session["logged_in"] = True

    return redirect(url_for("account.info"))

@account.route("/logout/", methods=["GET"])
def logout():
    session["logged_in"] = False
    session["uid"] = -1
    flash("Logout successful.", "info")
    return redirect(url_for('account.login'))

@account.route("/info/")
@require_login
def info():
    return redirect(url_for('volunteer.you'))

@account.before_app_request
def set_user():
    g.user = get_current_user()
