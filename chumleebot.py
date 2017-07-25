import sys
import discord
import re
import random
import json
import time

from resources.firebaseinfo import db
import resources.prawnsrars
import databasefunctions

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-----")
    await client.change_presence(game=discord.Game(name=random.choice(resources.prawnsrars.statuses)))

@client.event
async def on_message(msg):
    # Have the bot type whenever a command is entered.
    if msg.content.startswith("."):
        await client.send_typing(msg.channel)

    # Pong!
    if msg.content.startswith(".ping"):
        await client.send_message(msg.channel, "Hey " + msg.author.id)

    # Displays a help/welcome message to get users started.
    elif msg.content.startswith(".help"):
        welcomemsg = ("Hi! I'm Chumlee, and I run this pawn shop. To get started, "
        "use **.register** to register yourself in the database. "
        "Then use **.commands** to see what I can do")
        await client.send_message(msg.channel, welcomemsg)

    # Displays available commands and their uses.
    elif msg.content.startswith(".commands"):
        commandinfo = ("*:keyboard: Commands:*\n\n"
        "**.register:** register in the <:chumcoin:337841443907305473> database\n\n"
        "**.balance:** check your <:chumcoin:337841443907305473> balance\n\n"
        "**.appraise <text/attachment>:** get an appraisal for an item\n\n"
        "**.pay <@user> <amount>:** pay someone <:chumcoin:337841443907305473>s\n\n"
        "**.give <@user> <amount>:** (admin command) give a user <:chumcoin:337841443907305473>s\n\n"
        "**.item:** gets a random item from the _Pawn Stars: The Game_ Wiki\n\n"
        "**.kevincostner:** dances with swolves"
        )
        await client.send_message(msg.channel, commandinfo)

    # Registers a user in the database adding their UID to
    # the "users" node and setting an initial balance and
    # value for "isInDeal".
    elif msg.content.startswith(".register"):
        if not databasefunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "Okay, let's get you set up <@" + msg.author.id + ">!")

            newuserdata = {
                "balance": 20,
                "isInDeal": False
            }

            db.child("users").child(msg.author.id).set(newuserdata)
            await client.send_message(msg.channel, "Alright, you're all set. See you in the pawn shop!")
        else:
            print("ID " + msg.author.id + " already registered!")
            await client.send_message(msg.channel, "Looks like you're already registered <@" + msg.author.id + ">")


    # Gets a user's balance from the database and
    # prints it in the chat.
    elif msg.content.startswith(".balance"):
        if not databasefunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        else:
            balance = db.child("users").child(msg.author.id).child("balance").get()
            await client.send_message(msg.channel, "Your balance is " + str(balance.val()) + " <:chumcoin:337841443907305473>")

    # Takes money from the message author's balance
    # and places it in the balance of the user specified in
    # the first command argument.
    elif msg.content.startswith(".pay"):
        if not databasefunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        else:
            args = str.split(msg.content)
            print(args[1])

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .pay <user> <amount>")
            elif re.match("<@[0-9]*>", args[1]) is None:
                await client.send_message(msg.channel, "That doesn't look like a username.")
            elif not is_registered(re.sub("[^0-9]", "", args[1])):
                await client.send_message(msg.channel, "That user isn't registered!")
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

                    databasefunctions.withdraw(msg.author.id, amt)
                    databasefunctions.deposit(payee, amt)

    # Adds money to the balance of the user specified
    # in the first command argument. Only usable by users
    # with admin rank.
    elif msg.content.startswith(".give"):
        if not databasefunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        elif not str(msg.author.top_role) == "admin":
            await client.send_message(msg.channel, "You must be an admin to use .give")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .give <user> <amount>")
            elif re.match("<@[0-9]*>", args[1]) is None:
                await client.send_message(msg.channel, "That doesn't look like a username.")
            elif not databasefunctions.is_registered(re.sub("[^0-9]", "", args[1])):
                await client.send_message(msg.channel, "That user isn't registered!")
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
                    databasefunctions.deposit(payee, amt)

    # Starts an appraisal of a string or an attachment.
    # Based on random.random() a value is assigned and offered
    # to the author of the message. Also checks to make sure the
    # author does not already have and active appraisal, and that
    # they have not made a deal within the appraisal cooldown time.
    elif msg.content.startswith(".appraise"):
        dealstarttime = int(time.time())

        if not databasefunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first!")
        elif databasefunctions.is_in_deal(msg.author.id):
            await client.send_message(msg.channel, "Looks like you've already got a deal on the table!")
        elif databasefunctions.last_deal_time(msg.author.id) is not None and not (dealstarttime - databasefunctions.last_deal_time(msg.author.id)) >= 900:

            secondstonextdeal = 900 - (dealstarttime - databasefunctions.last_deal_time(msg.author.id))
            if secondstonextdeal <= 60:
                timetodealstring = "" + str(int(round(secondstonextdeal, 0))) + " more seconds"
            else:
                timetodealstring = "" + str(int(round(secondstonextdeal / 60, 0))) + " more minutes"

            await client.send_message(msg.channel, "You've gotta wait " + timetodealstring + " until your next deal.")
        else:
            seller = msg.author.id
            databasefunctions.set_deal_status(seller, True)

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
                databasefunctions.set_deal_status(seller, False)
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
                    databasefunctions.set_deal_status(seller, False)
                elif response.content == ".deal":
                    await client.send_message(msg.channel, "Cha-ching! <:chumcoin:337841443907305473><:chumcoin:337841443907305473><:chumcoin:337841443907305473>")
                    databasefunctions.deposit(msg.author.id, value)
                    databasefunctions.set_deal_status(seller, False)
                    databasefunctions.update_last_deal_time(seller)
                elif response.content == ".nodeal":
                    await client.send_message(msg.channel, "Alright, no deal then.")
                    databasefunctions.set_deal_status(seller, False)
                else:
                    await client.send_message(msg.channel, "Something went wrong!")
                    databasefunctions.set_deal_status(seller, False)

    # Posts a link to DaThings1's "Prawn Srars" along
    # with a random quote from the video.
    elif msg.content.startswith(".kevincostner"):
        await client.send_message(msg.channel, random.choice(resources.prawnsrars.ytpquotes))
        await client.send_message(msg.channel, "https://www.youtube.com/watch?v=5mEJbX5pio8")

    # Posts a random item from the Pawn Stars: The Game
    # wiki.
    elif msg.content.startswith(".item"):
        baseurl = "http://pawnstarsthegame.wikia.com"

        with open('resources/items.json') as data_file:
            data = json.load(data_file)

        await client.send_message(msg.channel, baseurl + data[random.randint(0, len(data) - 1)]["value"])


# Run the bot
client.run("MzM4NDIxOTMyNDI2OTE5OTM2.DFVLkA.oH1RXMJFxlFqi2BPgTwcUGKRiFs")
