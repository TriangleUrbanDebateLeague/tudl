from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from flask import current_app, flash, g, session, request

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

def send_error_email(env, trace):
    if not current_app.config["EMAIL_ERRORS"]:
        return

    info = dict(trace=trace, session=list(session.items()),
                form_data=list(request.form.items()), url=request.full_path,
                method=request.method, env=env)

    send_email(current_app.config["EMAIL_FROM"], current_app.config["SITE_ADMIN"], "Application error ({})".format(env),
    """
    The following exception occurred in {env}:

    {trace}

    Here is information that may be helpful in debugging the problem.

    URL: {url}

    Session data: {session}

    Form data: {form_data}

    Request method: {method}
    """.format(**info))
