import pyrebase
import requests
import os

url = "https://api.heroku.com/apps/chumlee-bot/config-vars"
headers = {
  "Accept": "application/vnd.heroku+json; version=3"
}

req = requests.get(url, headers=headers)
result = req.json()

config = {
  "apiKey": "AIzaSyAF0_Z_eSA0ICIvML2PouaCuizk3ADUWVg",
  "authDomain": "chumlee-bot.firebaseapp.com",
  "databaseURL": "https://chumlee-bot.firebaseio.com/",
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

firebase = pyrebase.initialize_app(config)
db = firebase.database()
