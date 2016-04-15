from flask import Flask, render_template

def create_app(environment):
    app = Flask(__name__)
    app.config.from_pyfile("config/{}.py".format(environment))

    from modules.account.blueprint import account
    from modules.staticpages.blueprint import staticpages
    from modules.donations.blueprint import donations

    app.register_blueprint(account)
    app.register_blueprint(donations)
    app.register_blueprint(staticpages)

    return app


if __name__ == '__main__':
    create_app("dev").run(port=5000, debug=True)
