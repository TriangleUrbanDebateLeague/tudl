import os

SEND_EMAIL = True
EMAIL_FROM = "test@unifieddemocracy.org"
APP_NAME = "Unified Democracy"
SECRET_KEY = "key"

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32))
STRIPE_KEY_SECRET = os.getenv("STRIPE_KEY_SECRET", "")
STRIPE_KEY_PUBLIC = os.getenv("STRIPE_KEY_PUBLIC", "")

DB_PATH = "/home/protected/tft.db"

EMAIL_ERRORS = False
SITE_ADMIN = ['foxwilson123@gmail.com']

SERVER_NAME = "test.teensforteens.info"

DISPLAY_DEBUG_INFO = False
ALLOW_RCON = False
