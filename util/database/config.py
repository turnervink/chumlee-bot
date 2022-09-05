import firebase_admin
from firebase_admin import db, credentials

import os
from os.path import exists
import sys

if not exists(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]):
    print(f"No Firebase credentials file at {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
    sys.exit(1)

default_app = firebase_admin.initialize_app(credentials.ApplicationDefault(), {
    "databaseURL": "https://chumlee-bot.firebaseio.com",
    "databaseAuthVariableOverride": {
        "uid": os.environ["DB_AUTH_UID"]
    }
})

db = db
db_root = os.environ["DB_ROOT"]
