from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from flask import flash

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("{} - {}".format(getattr(form, field).label.text, error), "error")

def send_email(from_, to, subject, text):
    message = MIMEText(text)
    message["From"] = from_
    message["To"] = to
    message["Subject"] = subject
    process = Popen(["/usr/bin/sendmail", "-t", "-oi"], stdin=PIPE)
    process.communicate(message.as_string().encode())
