import pyrebase
import os

config = {
    "apiKey": "AIzaSyAF0_Z_eSA0ICIvML2PouaCuizk3ADUWVg",
    "authDomain": "chumlee-bot.firebaseapp.com",
    "databaseURL": "https://chumlee-bot.firebaseio.com/" + os.environ["DB_ROOT"],
    "storageBucket": "chumlee-bot.appspot.com",
    "serviceAccount": {
        "type": "service_account",
        "project_id": "chumlee-bot",
        "private_key_id": os.environ["DB_PRIVATE_KEY_ID"],
        "private_key": os.environ["DB_PRIVATE_KEY"].replace('\\n', '\n'),
        "client_email": os.environ["DB_CLIENT_EMAIL"],
        "client_id": os.environ["DB_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-r5ehf%40chumlee-bot.iam.gserviceaccount.com"
    }
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
