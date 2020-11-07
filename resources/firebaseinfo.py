import pyrebase
import os


def noquote(s):
    return s


config = {
  "apiKey": "AIzaSyAF0_Z_eSA0ICIvML2PouaCuizk3ADUWVg",
  "authDomain": "chumlee-bot.firebaseapp.com",
  "databaseURL": "https://chumlee-bot.firebaseio.com/" + os.environ["location"],
  "storageBucket": "chumlee-bot.appspot.com",
  "serviceAccount": {
    "type": "service_account",
    "project_id": "chumlee-bot",
    "private_key_id": os.environ["private_key_id"],
    "private_key": os.environ["private_key"].replace('\\n', '\n'),
    "client_email": os.environ["client_email"],
    "client_id": os.environ["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-r5ehf%40chumlee-bot.iam.gserviceaccount.com"
  }
}

# Pyrebase is broken (see https://github.com/thisbejim/Pyrebase/issues/296), so this is a workaround
pyrebase.pyrebase.quote = noquote

firebase = pyrebase.initialize_app(config)
db = firebase.database()
