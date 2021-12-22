import firebase_admin
from firebase_admin import db, credentials

import json
import os

db_creds_file = open(os.environ["DB_CREDS_FILE"], "r")
db_creds = json.loads(db_creds_file.read())
db_creds["private_key_id"] = os.environ["DB_PRIV_KEY_ID"]
db_creds["private_key"] = os.environ["DB_PRIV_KEY"]

default_app = firebase_admin.initialize_app(credentials.Certificate(db_creds), {
    "databaseURL": "https://chumlee-bot.firebaseio.com",
    "databaseAuthVariableOverride": {
        "uid": os.environ["DB_AUTH_UID"]
    }
})

db = db
db_root = os.environ["DB_ROOT"]
