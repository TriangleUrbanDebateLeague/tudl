from flask import Flask, render_template, flash, redirect, make_response
from database import database
from utils import send_email, send_error_email
import traceback

import logging
log_formatter = logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
''')

def create_app(environment):
    app = Flask(__name__)
    app.config.from_pyfile("config/{}.py".format(environment))

    database.init(app.config["DB_PATH"])

    if app.config["EMAIL_ERRORS"]:
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1', app.config["EMAIL_FROM"], app.config["SITE_ADMIN"], 'Exception in TFT-{}'.format(environment))
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(log_formatter)
        app.logger.addHandler(mail_handler)

    from modules.account.blueprint import account
    from modules.staticpages.blueprint import staticpages
    from modules.donations.blueprint import donations
    from modules.volunteer.blueprint import volunteer

    app.register_blueprint(account)
    app.register_blueprint(volunteer)
    app.register_blueprint(donations)
    app.register_blueprint(staticpages) # staticpages must be registered last

    @app.route("/favicon.ico")
    def favicon(): return redirect('/static/favicon.ico')

    @app.route("/robots.txt")
    def robots_txt(): return redirect('/static/robots.txt')

    @app.route("/teensforteens.info.html")
    def verify_cert(): return "MTRHYzBuSUg3TU1DSnNiZzJqZHo0WXllWnc0NVB3OWE4MmpUd0ZGa0dSdz0"

    @app.route("/googlefe31abc06e03d8f7.html")
    def google(): return "google-site-verification: googlefe31abc06e03d8f7.html"

    @app.errorhandler(500)
    def internal_error(exc):
        trace = traceback.format_exc()
        try:
            send_error_email(environment, trace)
        except:
            trace = traceback.format_exc()
        return make_response(render_template("whoops.html", trace=trace), 500)

    return app

if __name__ == '__main__':
    create_app("dev").run(port=5000, debug=True)
