# Teens for Teens framework

## What is this?
This is the code that runs the Teens for Teens platform. You can find the
`master` branch live at [the Teens for Teens website](https://teensforteens.info).

## What do I do if I find a bug?
If you find a bug, that is not security-related, you should report it on GitHub
by creating a new issue. If the bug is security-related, **do not file a GitHub
issue**. Instead, follow the directions below.

If you find a security-related bug (for example, if user or volunteer
information is disclosed to someone who shouldn't have it), you should send me an
email at `foxwilson123@gmail.com`. Please don't publically disclose the bug or
exploit it beyond what you need to report it to me. Use common sense and handle
this responsibly, please. If you'd like to PGP-encrypt your bug report, my key
is:

    pub   rsa4096/73DDD719 2016-02-15 [SC] [expires: 2018-02-14]
    Key fingerprint = C751 1F5E 5650 CB9A 5246  37FF 42F2 7EB2 73DD D719

## External services / API keys you need
The platform relies on [Stripe](https://stripe.com) in order to handle
donations. If you're not accepting donations, you don't have to worry about
this.

You also need a working `sendmail` in order to send email confirmations of
accounts and other email-requiring features.

## General project architecture
The project is built on the Flask web framework, using Peewee as an ORM and
WTForms for form rendering and validation. If you are unfamiliar with these
technologies, you should learn them, as they are fairly critical to the
application.

The database used in production is SQLite. I'm sure I'll regret this later.

The `testing` and `master` branches are hosted on
[NearlyFreeSpeech.NET](https://nearlyfreespeech.net), because it's my favorite
web host and they are fairly low-cost. If you plan to set up a production
instance of the platform for your organization, I highly recommend them. The
`nfsn.sh` script is designed for use on their platform.

### Components
The platform is composed of several distinct components. Separation between
these components is achieved using Flask's Blueprint functionality. Each
component has its own directory in `site/modules`, with its own set of
templates, forms, and routes. The only part that does not follow this pattern
is the database model definition component, which is located in
`site/database.py`.

#### `staticpages`
This is probably the easiest module to understand. It renders the template
requested in the URL:

    @staticpages.route("/", defaults={"page": "index"})
    @staticpages.route("/<page>/")
    def show_staticpage(page):
        try:
            return render_template("{}.html".format(page))
        except:
            return make_response(render_template("not_found.html"), 404)

#### `donations`
This is the module which accepts donations. It uses Stripe.js in order to not
have to worry about credit card information, and keeps track of those who have
donated in the database in order to comply with FEC regulations.

#### `account`
This is the module which handles user accounts. Users can create and manage
their accounts with this module. This is very separate from the `volunteer`
module.

#### `volunteer`
This module handles volunteer hour tracking. Volunteers can either be associated
with an account or not ("local volunteers"). Volunteers can be associated with
accounts after account registration or during account registration, and are
completely separate entities from accounts.

## Application initialization
This section describes the process for application initialization, and is
generally a helpful resource to consult if something is going wrong during that
phase.

### Development server
If the development server is started with e.g. `python app.py`, the following
process is followed:

- the `dev` environment is used
- the application is initialized
- the application is run in debug mode

### Test or Production server
If the server is started with e.g. `nfsn.sh` then the following procedure is
used.

- a file containing configuration keys in environment variables is sourced
- a virtualenv with application dependencies is activated
- the app environment is set in the `APP_ENVIRONMENT` environment variable
- `gunicorn` calls `tftwsgi` to create the application
- `tftwsgi` creates the application with the app environment set in the
  `APP_ENVIRONMENT` environment variable
- the application is initialized
- gunicorn starts workers to handle application requests

### Initialization procedure
In the previous sections, "the application is initialized" refers to the
following process.

- the application loads environment-specific configuration from the appropriate
  configuration file
- the database configuration is set
- application components are loaded and registered
- a 500 error handler is attached

## Database stuff
To create database tables:

    platform $ cd site
    platform/site $ python manage.py -e {environment} create_db
