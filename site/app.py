from flask import Flask, render_template, flash, redirect
from database import database

def create_app(environment):
    app = Flask(__name__)
    app.config.from_pyfile("config/{}.py".format(environment))

    database.init(app.config["DB_PATH"])

    if app.config["EMAIL_ERRORS"]:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1', app.config["EMAIL_FROM"], app.config["SITE_ADMIN"], 'Exception in TFT-{}'.format(environment))
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    from modules.account.blueprint import account
    from modules.staticpages.blueprint import staticpages
    from modules.donations.blueprint import donations

    app.register_blueprint(donations)

    app.register_blueprint(staticpages) # staticpages must be registered last

    @app.route("/favicon.ico")
    def favicon(): return redirect('/static/favicon.ico')

    return app

if __name__ == '__main__':
    create_app("dev").run(port=5000, debug=True)
