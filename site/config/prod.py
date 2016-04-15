import os

SEND_EMAIL = True
EMAIL_FROM = "site@teensforteens.info"
APP_NAME = "Teens for Teens"
SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32))
