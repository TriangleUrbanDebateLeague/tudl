import os

SEND_EMAIL = True
EMAIL_FROM = "dev@local.dev"
APP_NAME = "Teens for Teens"
SECRET_KEY = "key"

STRIPE_KEY_SECRET = os.getenv("STRIPE_KEY_SECRET", "")
STRIPE_KEY_PUBLIC = os.getenv("STRIPE_KEY_PUBLIC", "")

DB_PATH = "tft.db"

EMAIL_ERRORS = False

DISPLAY_DEBUG_INFO = False
ALLOW_RCON = False

def send_email(from_, to, subject, text):
    print("From: {}".format(from_))
    print("To: {}".format(to))
    print("Subject: {}".format(subject))
    print("Text: {}".format(text))
