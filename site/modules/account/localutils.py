import random
import smtplib
import string

from .models import Account, PasswordReset
from modules.volunteer.models import Volunteer
from datetime import datetime
from flask import current_app, url_for, session
from utils import send_email
from peewee import IntegrityError

valid_chars = string.ascii_letters + string.digits

confirm_email_template = """Hi {first_name},
Thanks for signing up for {application}. Please click the following
link (or copy and paste it into your browser) in order to verify your email:

{confirm_email_link}

If you did not create an account on {application}, please ignore this email."""

reset_password_template = """Hi {first_name},
You (or someone pretending to be you) has requested a password reset for your
{application} account. If this was you, you can click the link below (or copy
and paste it into your browser) to reset your password:

{reset_password_link}

If you did not request a password reset for {application}, please ignore this.
No action is required."""

def generate_confirmation_key(n=64):
    return "".join([random.choice(valid_chars) for i in range(n)])

def send_confirm_email(first_name, email):
    if not current_app.config['SEND_EMAIL']:
        return None

    confirm_key = generate_confirmation_key()
    confirm_email_link = url_for('account.confirm_email', key=confirm_key, _external=True)
    message = confirm_email_template.format(first_name=first_name,
                                            application=current_app.config['APP_NAME'],
                                            confirm_email_link=confirm_email_link)
    send_email(current_app.config['EMAIL_FROM'], email,
               "Please confirm your {} account".format(current_app.config['APP_NAME']), message)

    return confirm_key

def send_reset_email(account):
    reset_key = generate_confirmation_key(n=128)
    PasswordReset.create(account=account, key=reset_key, created_at=datetime.now(), used=False)

    reset_link = url_for('account.reset_password', key=reset_key, _external=True)
    message = reset_password_template.format(first_name=account.first_name,
                                             application=current_app.config['APP_NAME'],
                                             reset_password_link=reset_link)

    if current_app.config['SEND_EMAIL']:
        send_email(current_app.config['EMAIL_FROM'], account.email,
                   "Password reset requested for your {} account".format(current_app.config['APP_NAME']), message)

def get_current_user():
    if "uid" in session and session["logged_in"]:
        return Account.get(Account.id == session["uid"])
    return None

def attach_volunteer(account):
    if account.volunteer is None:
        query = Volunteer.select().where(Volunteer.account == None & Volunteer.local_first_name == account.first_name & Volunteer.local_last_name == account.last_name)
        if query.count() == 1:
            volunteer = next(query.iterator())
            volunteer.account = account
            volunteer.save()
            return volunteer
        else:
            return Volunteer.create(account=account)
    raise IntegrityError("Account with id {} already has an associated Volunteer, but attach_volunteer was called".format(account.id))
