import os

SEND_EMAIL = False
APP_NAME = "Teens for Teens"
SECRET_KEY = "key"

STRIPE_KEY_SECRET = os.getenv("STRIPE_KEY_SECRET", "")
STRIPE_KEY_PUBLIC = os.getenv("STRIPE_KEY_PUBLIC", "")

DB_PATH = "tft.db"

EMAIL_ERRORS = False

DISPLAY_DEBUG_INFO = True
