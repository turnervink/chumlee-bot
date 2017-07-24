import discord
import asyncio
import pyrebase
import re
import random
from prawnsrars import ytpquotes

config = {
  "apiKey": "AIzaSyAF0_Z_eSA0ICIvML2PouaCuizk3ADUWVg",
  "authDomain": "chumlee-bot.firebaseapp.com",
  "databaseURL": "https://chumlee-bot.firebaseio.com/",
  "storageBucket": "chumlee-bot.appspot.com",
  "serviceAccount": "chumlee-bot-firebase-adminsdk-r5ehf-2fca8ef380.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

client = discord.Client()

def is_registered(id):
    dbusername = db.child("users").child(id).get()
    if dbusername.val() is None:
        print("returning false")
        return False
    else:
        print("returning true")
        return True

def deposit(id, amt):
    currentbalance = db.child("users").child(id).child("balance").get()
    newbalance = currentbalance.val() + amt
    db.child("users").child(id).child("balance").set(newbalance)

def withdraw(id, amt):
    currentbalance = db.child("users").child(id).child("balance").get()
    newbalance = currentbalance.val() - amt
    db.child("users").child(id).child("balance").set(newbalance)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-----")
    await client.change_presence(game=discord.Game(name='Collecting shoes'))

@client.event
async def on_message(msg):

    if msg.content.startswith(".ping"):
        await client.send_message(msg.channel, "Hey " + msg.author.id)

    elif msg.content.startswith(".help"):
        welcomemsg = ("Hi! I'm Chumlee, and I run this pawn shop. To get started, "
        "use **.register** to register yourself in the database. "
        "Then use **.commands** to see what I can do")
        await client.send_message(msg.channel, welcomemsg)

    elif msg.content.startswith(".commands"):
        commandinfo = ("*Commands:*\n"
        "**.register:** register in the <:chumcoin:337841443907305473> database\n"
        "**.balance:** check your <:chumcoin:337841443907305473> balance\n"
        "**.pay <user> <amount>:** pay someone <:chumcoin:337841443907305473>s\n"
        )
        await client.send_message(msg.channel, commandinfo)

    elif msg.content.startswith(".register"):
        if not is_registered(msg.author.id):
            await client.send_message(msg.channel, "Okay, let's get you set up <@" + msg.author.id + ">!")

            newuserdata = {"balance": 20}

            db.child("users").child(msg.author.id).set(newuserdata)
            await client.send_message(msg.channel, "Alright, you're all set. See you in the pawn shop!")
        else:
            print("ID " + msg.author.id + " already registered!")
            await client.send_message(msg.channel, "Looks like you're already registered <@" + msg.author.id + ">")

    elif msg.content.startswith(".balance"):
        if not is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        else:
            balance = db.child("users").child(msg.author.id).child("balance").get()
            await client.send_message(msg.channel, "Your balance is " + str(balance.val()) + " <:chumcoin:337841443907305473>")

    elif msg.content.startswith(".pay"):
        if not is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .pay <user> <amount>")
            else:
                print(args)
                payee = re.sub("[^0-9]", "", args[1])
                try:
                    amt = int(args[2])
                except:
                    await client.send_message(msg.channel, "You can only pay amounts that are whole numbers")
                    amt = -1

                payerbalance = db.child("users").child(msg.author.id).child("balance").get()
                payeebalance = db.child("users").child(payee).child("balance").get()
                newpayeebalance = payeebalance.val() + amt
                newpayerbalance = payerbalance.val() - amt

                if amt == -1:
                    # amt wasn't an int, do nothing
                    print()
                elif payee == msg.author.id:
                    await client.send_message(msg.channel, "You can't pay yourself!")
                elif amt > payerbalance.val():
                    await client.send_message(msg.channel, "Sorry, you don't have enough chumcoins for that!")
                elif amt <= 0:
                    await client.send_message(msg.channel, "You can only pay amounts above 0")
                else:
                    await client.send_message(msg.channel, "Okay! Paying " + args[1] + " " + args[2] + " <:chumcoin:337841443907305473>")

                    withdraw(msg.author.id, amt)
                    deposit(payee, amt)

    elif msg.content.startswith(".give"):
        if not is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        elif not str(msg.author.top_role) == "admin":
            await client.send_message(msg.channel, "You must be an admin to use .give")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .give <user> <amount>")
            else:
                print(args)
                payee = re.sub("[^0-9]", "", args[1])
                try:
                    amt = int(args[2])
                except:
                    await client.send_message(msg.channel, "You can only give amounts that are whole numbers")
                    amt = -1

                payeebalance = db.child("users").child(payee).child("balance").get()
                newpayeebalance = payeebalance.val() + amt

                if amt == -1:
                    # amt wasn't an int, do nothing
                    print()
                else:
                    await client.send_message(msg.channel, "Giving " + args[1] + " " + args[2] + " <:chumcoin:337841443907305473>")
                    deposit(payee, amt)

    elif msg.content.startswith(".appraise"):
        if not is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        else:
            seller = msg.author.id

            args = str.split(msg.content)
            files = msg.attachments

            random.seed()
            base = random.random()

            if base > 0.99:
                value = random.randint(500, 1000)
                itemclass = "Holy cow! That's one valuable item!"
            elif base > 0.8:
                value = random.randint(250, 500)
                itemclass = "Wow! I've got to have this."
            elif base > 0.75:
                value = random.randint(100, 250)
                itemclass = "That's a nice piece you've got there."
            elif base > 0.5:
                value = random.randint(10, 100)
                itemclass = "Hmm... I guess I'll take it."
            elif base > 0.15:
                value = random.randint(1, 10)
                itemclass = "Well, it's nothing special"
            else:
                itemclass = "I'm sorry, but no deal"
                value = 0

            if len(args) == 1 and len(files) == 0:
                await client.send_message(msg.channel, "You must include something to appraise")
            elif len(files) != 0:
                print("appraising file")
                await client.send_message(msg.channel, itemclass)
                await client.send_message(msg.channel, "Offer: " + str(value) + " <:chumcoin:337841443907305473>")
            else:
                print("appraising text")
                await client.send_message(msg.channel, itemclass)
                await client.send_message(msg.channel, "Offer: " + str(value) + " <:chumcoin:337841443907305473>")

            await client.send_message(msg.channel, "Use .deal/.nodeal to accept/decline the offer in the next 30 seconds")

            def check(msg):
                return msg.content == ".deal" or msg.content == ".nodeal"

            response = await client.wait_for_message(timeout = 30.0, author = msg.author, check = check)
            if response is None:
                await client.send_message(msg.channel, "Alright, no deal then.")
            elif response.content == ".deal":
                await client.send_message(msg.channel, "Cha-ching! <:chumcoin:337841443907305473><:chumcoin:337841443907305473><:chumcoin:337841443907305473>")
                deposit(msg.author.id, value)
            elif response.content == ".nodeal":
                await client.send_message(msg.channel, "Alright, no deal then.")
            else:
                await client.send_message(msg.channel, "Something went wrong!")

    elif msg.content.startswith(".kevincostner"):
        await client.send_message(msg.channel, random.choice(ytpquotes))
        await client.send_message(msg.channel, "https://www.youtube.com/watch?v=5mEJbX5pio8")


# Run
client.run("MzM4NDIxOTMyNDI2OTE5OTM2.DFVLkA.oH1RXMJFxlFqi2BPgTwcUGKRiFs")
