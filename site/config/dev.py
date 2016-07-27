import os

SEND_EMAIL = True
EMAIL_FROM = "dev@local.dev"
APP_NAME = "Unified Democracy"
SECRET_KEY = "key"

STRIPE_KEY_SECRET = os.getenv("STRIPE_KEY_SECRET", "")
STRIPE_KEY_PUBLIC = os.getenv("STRIPE_KEY_PUBLIC", "")

DB_PATH = "tft.db"

EMAIL_ERRORS = False

DISPLAY_DEBUG_INFO = False
ALLOW_RCON = False

DEV_EMAIL = True
