import sys
import discord
import re
import random
import json
import time

from resources.firebaseinfo import db
import resources.prawnsrars
import dbfunctions
import functions
import resources.medalprices
medalprices = resources.medalprices

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

    # Displays a help/welcome message to get users started.
    if msg.content.startswith(".help"):
        welcomemsg = ("Hi! I'm Chumlee, and I run this pawn shop. To get started, "
        "use **.register** to register yourself in the database. "
        "Then use **.commands** to see what I can do")
        await client.send_message(msg.channel, welcomemsg)

    # Displays available commands and their uses.
    elif msg.content.startswith(".commands"):
        commandinfo = ("*Commands* :keyboard::\n\n"
        "**.register:** register in the <:chumcoin:337841443907305473> database\n\n"
        "**.balance:** check your <:chumcoin:337841443907305473> balance\n\n"
        "**.appraise <text/attachment>:** get an appraisal for an item\n\n"
        "**.pay <@user> <amount>:** pay someone <:chumcoin:337841443907305473>s\n\n"
        "**.give <@user> <amount>:** (admin command) give a user <:chumcoin:337841443907305473>s\n\n"
        "**.item:** gets a random item from the _Pawn Stars: The Game_ Wiki\n\n"
        "**.purge:** delete chumlee-bot's messages from the last 100 messages\n\n"
        "**.kevincostner:** dances with swolves"
        )
        await client.send_message(msg.channel, commandinfo)

    # Registers a user in the database adding their UID to
    # the "users" node and setting an initial balance and
    # value for "isInDeal".
    elif msg.content.startswith(".register"):
        if not dbfunctions.is_registered(msg.author.id):
            newuserdata = {
                "balance": 20,
                "isInDeal": False,
                "medals": {
                    "tin": False,
                    "bronze": False,
                    "silver": False,
                    "gold": False,
                    "platinum": False
                }
            }

            db.child("users").child(msg.author.id).set(newuserdata)
            await client.send_message(msg.channel, "Okay, you're all set up " + msg.author.mention + "!")
        else:
            await client.send_message(msg.channel, "Looks like you're already registered " + msg.author.mention + ".")

    # Gets a user's balance from the database and
    # prints it in the chat.
    elif msg.content.startswith(".balance"):
        if not dbfunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first " + msg.author.mention + "!")
        else:
            # balance = db.child("users").child(msg.author.id).child("balance").get()
            await client.send_message(msg.channel, "Your balance is " + str(dbfunctions.get_balance(msg.author.id)) + " <:chumcoin:337841443907305473>")

    # Takes money from the message author's balance
    # and places it in the balance of the user specified in
    # the first command argument.
    elif msg.content.startswith(".pay"):
        if not dbfunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first " + msg.author.mention + "!")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .pay <user> <amount>")
            elif functions.is_valid_userid(args[1]) is None:
                await client.send_message(msg.channel, "That doesn't look like a username.")
            elif not dbfunctions.is_registered(re.sub("[^0-9]", "", args[1])):
                await client.send_message(msg.channel, "That user isn't registered!")
            else:
                payee = re.sub("[^0-9]", "", args[1])
                try:
                    amt = int(args[2])
                except:
                    # TODO Move this up to the first if/else of this command
                    await client.send_message(msg.channel, "You can only pay amounts that are whole numbers")
                    amt = -1

                if amt == -1:
                    # amt wasn't an int, do nothing
                    print()
                elif payee == msg.author.id:
                    await client.send_message(msg.channel, "You can't pay yourself!")
                elif not dbfunctions.check_for_funds(msg.author.id, amt):
                    await client.send_message(msg.channel, "Sorry, you don't have enough chumcoins for that!")
                elif amt <= 0:
                    await client.send_message(msg.channel, "You can only pay amounts above 0")
                else:
                    await client.send_message(msg.channel, "" + msg.author.mention + "  :arrow_right:  <:chumcoin:337841443907305473> x" + args[2] + "  :arrow_right:  " + args[1])

                    dbfunctions.withdraw(msg.author.id, amt)
                    dbfunctions.deposit(payee, amt)

    # Adds money to the balance of the user specified
    # in the first command argument. Only usable by users
    # with admin rank.
    elif msg.content.startswith(".give"):
        if not dbfunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first " + msg.author.mention + "!")
        elif not str(msg.author.top_role) == "admin":
            await client.send_message(msg.channel, "You must be an admin to use .give")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .give <user> <amount>")
            elif functions.is_valid_userid(args[1]) is None:
                await client.send_message(msg.channel, "That doesn't look like a username.")
            elif not dbfunctions.is_registered(re.sub("[^0-9]", "", args[1])):
                await client.send_message(msg.channel, "That user isn't registered!")
            else:
                payee = re.sub("[^0-9]", "", args[1])
                try:
                    amt = int(args[2])
                except:
                    #TODO Move this up
                    await client.send_message(msg.channel, "You can only give amounts that are whole numbers")
                    amt = -1

                if amt == -1:
                    # amt wasn't an int, do nothing
                    print()
                else:
                    await client.send_message(msg.channel, "<:chumcoin:337841443907305473> x" + args[2] + "  :arrow_right:  " + args[1])
                    dbfunctions.deposit(payee, amt)

    # Starts an appraisal of a string or an attachment.
    # Based on random.random() a value is assigned and offered
    # to the author of the message. Also checks to make sure the
    # author does not already have and active appraisal, and that
    # they have not made a deal within the appraisal cooldown time.
    elif msg.content.startswith(".appraise"):
        now = int(time.time())

        if not dbfunctions.is_registered(msg.author.id):
            await client.send_message(msg.channel, "You need to use **.register** first " + msg.author.mention + "!")
        elif dbfunctions.is_in_deal(msg.author.id):
            await client.send_message(msg.channel, "Looks like you've already got a deal on the table " + msg.author.mention + "!")
        elif dbfunctions.last_deal_time(msg.author.id) is not None and not functions.in_cooldown_period(msg.author.id):

            secondstonextdeal = 900 - (now - dbfunctions.last_deal_time(msg.author.id))
            if secondstonextdeal <= 60:
                timetodealstring = "" + str(int(round(secondstonextdeal, 0))) + " more seconds"
            else:
                timetodealstring = "" + str(int(round(secondstonextdeal / 60, 0))) + " more minutes"

            await client.send_message(msg.channel, "You've gotta wait " + timetodealstring + " until your next deal " + msg.author.mention + ".")
        else:
            seller = msg.author.id
            dbfunctions.set_deal_status(seller, True)

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
                dbfunctions.set_deal_status(seller, False)
            else:
                print("appraising text")
                await client.send_message(msg.channel, itemclass)
                await client.send_message(msg.channel, msg.author.mention + " Offer: " + str(value) + " <:chumcoin:337841443907305473> (.deal/.nodeal)")

                # await client.send_message(msg.channel, "Use .deal/.nodeal to accept/decline the offer in the next 30 seconds")

                def check(i):
                    return i.content == ".deal" or i.content == ".nodeal"

                response = await client.wait_for_message(timeout=30.0, author=msg.author, check=check)
                if response is None:
                    await client.send_message(msg.channel, "Alright, no deal then.")
                    dbfunctions.set_deal_status(seller, False)
                elif response.content == ".deal":
                    await client.send_message(msg.channel, "Cha-ching!")
                    await client.send_message(msg.channel, "<:chumlee:337842115931537408>  :arrow_right:  <:chumcoin:337841443907305473> x" + str(value) + "  :arrow_right:  " + msg.author.mention)
                    dbfunctions.deposit(msg.author.id, value)
                    dbfunctions.set_deal_status(seller, False)
                    dbfunctions.update_last_deal_time(seller)
                elif response.content == ".nodeal":
                    await client.send_message(msg.channel, "Alright, no deal then.")
                    dbfunctions.set_deal_status(seller, False)
                else:
                    await client.send_message(msg.channel, "Something went wrong!")
                    dbfunctions.set_deal_status(seller, False)

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

    # Deletes chumlee-bot messages sent in the last
    # 100 messages.
    elif msg.content.startswith(".purge"):
        def check(i):
            return i.author.id == client.user.id

        try:
            await client.purge_from(channel=msg.channel, limit=100, check=check)
            await client.send_message(msg.channel, "Purged from last 100 messages :put_litter_in_its_place:")
        except discord.errors.Forbidden:
            await client.send_message(msg.channel, "I need permission to manage messages in order to use .purge!")

    # Sends a file displaying the available Chummedals
    # and their prices.
    elif msg.content.startswith(".listmedals"):
        await client.send_file(msg.channel, "resources/img/medals/chummedal-row.png")

    # Lists a user's medals.
    elif msg.content.startswith(".mymedals"):
        # medalslist = []
        medalslist = ""
        # medals = db.child("users").child(msg.author.id).child("medals").order_by_value().equal_to(True).get()
        medals = dbfunctions.get_medals(msg.author.id)
        for medal in medals:
            print(medal)
            # medalslist.append(i)
            medalslist += " " + medal

        await client.send_message(msg.channel, msg.author.mention + "'s medals:")
        # for i in medalslist:
            # await client.send_file(msg.channel, "resources/img/medals/" + i + "chum64.png")
        await client.send_message(msg.channel, medalslist)

    # Lets a user buy a Chummedal and sets
    # it to True in the "medals" node of their database
    # entry.
    elif msg.content.startswith(".buymedal"):
        args = str.split(msg.content)

        if not len(args) == 2:
            await client.send_message(msg.channel, "Usage: .buymedal <medal>")
        else:
            if str.lower(args[1]) == "tin":
                if dbfunctions.check_for_funds(msg.author.id, medalprices.tin):
                    await client.send_message(msg.channel, "Alright! Here's a tin medal for you!")
                    dbfunctions.withdraw(msg.author.id, medalprices.tin)
                    await client.send_message(msg.channel, msg.author.mention + "  :arrow_right:  <:chumcoin:337841443907305473> x" + str(medalprices.tin) + "  :arrow_right:  <:chumlee:337842115931537408>")
                    dbfunctions.award_medal(msg.author.id, "tin")
                else:
                    await client.send_message(msg.channel, "You don't have enough Chumcoins for a tin medal!")
            elif str.lower(args[1]) == "bronze":
                if dbfunctions.check_for_funds(msg.author.id, medalprices.bronze):
                    await client.send_message(msg.channel, "Alright! Here's a bronze medal for you!")
                    dbfunctions.withdraw(msg.author.id, medalprices.bronze)
                    await client.send_message(msg.channel, msg.author.mention + "  :arrow_right:  <:chumcoin:337841443907305473> x" + str(medalprices.bronze) + "  :arrow_right:  <:chumlee:337842115931537408>")
                    dbfunctions.award_medal(msg.author.id, "bronze")
                else:
                    await client.send_message(msg.channel, "You don't have enough Chumcoins for a bronze medal!")
            elif str.lower(args[1]) == "silver":
                if dbfunctions.check_for_funds(msg.author.id, medalprices.silver):
                    await client.send_message(msg.channel, "Alright! Here's a silver medal for you!")
                    await client.send_message(msg.channel, msg.author.mention + "  :arrow_right:  <:chumcoin:337841443907305473> x" + str(medalprices.silver) + "  :arrow_right:  <:chumlee:337842115931537408>")
                    dbfunctions.withdraw(msg.author.id, medalprices.silver)
                    dbfunctions.award_medal(msg.author.id, "silver")
                else:
                    await client.send_message(msg.channel, "You don't have enough Chumcoins for a silver medal!")
            elif str.lower(args[1]) == "gold":
                if dbfunctions.check_for_funds(msg.author.id, medalprices.gold):
                    await client.send_message(msg.channel, "Alright! Here's a gold medal for you!")
                    await client.send_message(msg.channel, msg.author.mention + "  :arrow_right:  <:chumcoin:337841443907305473> x" + str(medalprices.gold) + "  :arrow_right:  <:chumlee:337842115931537408>")
                    dbfunctions.withdraw(msg.author.id, medalprices.gold)
                    dbfunctions.award_medal(msg.author.id, "gold")
                else:
                    await client.send_message(msg.channel, "You don't have enough Chumcoins for a gold medal!")
            elif str.lower(args[1]) == "platinum":
                if dbfunctions.check_for_funds(msg.author.id, medalprices.platinum):
                    await client.send_message(msg.channel, "Alright! Here's a platinum medal for you!")
                    await client.send_message(msg.channel, msg.author.mention + "  :arrow_right:  <:chumcoin:337841443907305473> x" + str(medalprices.platinum) + "  :arrow_right:  <:chumlee:337842115931537408>")
                    dbfunctions.withdraw(msg.author.id, medalprices.platinum)
                    dbfunctions.award_medal(msg.author.id, "platinum")
                else:
                    await client.send_message(msg.channel, "You don't have enough Chumcoins for a platinum medal!")
            else:
                await client.send_message(msg.channel, "There isn't a medal called " + args[1] + ".")


# Run the bot
client.run("MzM4NDIxOTMyNDI2OTE5OTM2.DFVLkA.oH1RXMJFxlFqi2BPgTwcUGKRiFs")
