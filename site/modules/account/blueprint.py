from flask import Blueprint, current_app, request, render_template, flash

from utils import flash_errors
from .forms import AccountCreateForm, AccountLoginForm, AccountPasswordResetForm
from database import Account, PasswordReset

account = Blueprint("account", __name__, template_folder="templates/account", url_prefix="/account")

@account.route("/create/", methods=["GET", "POST"])
def create_account():
    form = AccountCreateForm(request.form)
    flash_errors(form)

    if not form.validate_on_submit():
        return render_template("create.html", form=form)

    existing_accounts = Account.select().where(Account.email == form.email.data)
    if existing_accounts.count() > 0:
        flash("An account already exists with that email address.", "error")
        return render_template("create.html", form=form)

    if current_app.config['SEND_EMAIL']:
        email_confirmed = False
        email_confirm_key = send_confirm_email(form.first_name.data, form.email.data)
    else:
        email_confirmed = True
        email_confirm_key = None

    password = Account.hash_password(form.password.data)

    account = Account.create(first_name=form.first_name.data, last_name=form.last_name.data,
                             email=form.email.data, email_confirm_key=email_confirm_key,
                             email_confirmed=email_confirmed, password=password)
