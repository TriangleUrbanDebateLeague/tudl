from flask import Blueprint, current_app, request, render_template, flash, session, redirect, url_for

from utils import flash_errors
from .forms import AccountCreateForm, AccountLoginForm, AccountPasswordResetForm
from database import Account, PasswordReset

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
                             state=form.state.data, email=form.email.data,
                             email_confirm_key=email_confirm_key, email_confirmed=email_confirmed,
                             password=password)

    return redirect(url_for('account.login'))

@account.route("/confirm_email/<key>/")
def confirm_email(key):
    matching_accounts = Account.select().where(Account.email_confirmed == False, Account.email_confirm_key == key)

    if matching_accounts.count() != 1:
        flash("Incorrect data.", "error")
    else:
        account = next(matching_accounts)
        account.email_confirmed = True
        account.save()
        flash("Email confirmed.", "success")

    return redirect(url_for('account.login'))

@account.route("/login/", methods=["GET", "POST"])
def login():
    form = AccountLoginForm(request.form)

    if not form.validate_on_submit():
        flash_errors(form)
        return render_template("login.html", form=form)

    matching_accounts = Account.select().where(Account.email == form.email.data)
    if matching_accounts.count() == 1:
        account = next(matching_accounts.iterator())
        print("Found an account...")
        if account.validate_password(form.password.data):
            flash("Login success.", "success")
            session["uid"] = account.id
            session["logged_in"] = True
            return redirect(url_for('account.info'))

    flash("Login failed.", "error")
    return render_template("login.html", form=form)

@account.route("/info/")
def info():
    return str(session["uid"])
