import pyrebase

config = {
  "apiKey": "AIzaSyAF0_Z_eSA0ICIvML2PouaCuizk3ADUWVg",
  "authDomain": "chumlee-bot.firebaseapp.com",
  "databaseURL": "https://chumlee-bot.firebaseio.com/",
  "storageBucket": "chumlee-bot.appspot.com",
  "serviceAccount": "resources/chumlee-bot-firebase-adminsdk-r5ehf-2fca8ef380.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
