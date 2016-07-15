from flask import current_app, url_for
from utils import send_email
import random
import string

valid_chars = string.ascii_letters + string.digits

confirm_email_template = """Hi,
Thanks for signing up for the {application} mailing list. Please click the
following link (or copy and paste it into your browser) in order to verify
your email:

{confirm_email_link}

If you did not subscribe to the {application} mailing list, please ignore this
email."""

def generate_confirmation_key(n=64):
    return "".join([random.choice(valid_chars) for i in range(n)])

def send_confirm_email(email):
    if not current_app.config["SEND_EMAIL"]:
        return None

    confirm_key = generate_confirmation_key()
    confirm_email_link = url_for("email_list.confirm_email", key=confirm_key, _external=True)
    message = confirm_email_template.format(application=current_app.config["APP_NAME"],
                                            confirm_email_link=confirm_email_link)

    send_email(current_app.config["EMAIL_FROM"], email,
               "Please confirm your mailing list subscription".format(current_app.config["APP_NAME"]), message)

    return confirm_key
