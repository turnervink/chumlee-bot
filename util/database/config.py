import firebase_admin
from firebase_admin import db, credentials

import os

cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://chumlee-bot.firebaseio.com",
    "databaseAuthVariableOverride": {
        "uid": os.environ["DB_AUTH_UID"]
    }
})

db = db
db_root = os.environ["DB_ROOT"]
