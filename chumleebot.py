import discord
import re
import random
import json
import time

import functions
import dbfunctions
from resources.firebaseinfo import db
import resources.prawnsrars
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
                       "**.take <@user> <amount>:** (admin command) take a user's <:chumcoin:337841443907305473>s\n\n"
                       "**.listmedals:** see available Chummedals\n\n"
                       "**.mymedals:** see your Chummedals\n\n"
                       "**.buymedal <medal>:** buy a Chummedal\n\n"
                       "**.item:** gets a random item from the _Pawn Stars: The Game_ Wiki\n\n"
                       "**.purge:** delete chumlee-bot's messages from the last 100 messages\n\n"
                       "**.kevincostner:** dances with swolves"
                       )
        await client.send_message(msg.channel, commandinfo)

    # Registers a user in the database adding their UID to
    # the "users" node and setting an initial balance and
    # value for "isInDeal".
    elif msg.content.startswith(".register"):
        if not dbfunctions.is_registered(msg.author):
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
        if not dbfunctions.is_registered(msg.author):
            await client.send_message(msg.channel, "You need to use **.register** first " + msg.author.mention + "!")
        else:
            # balance = db.child("users").child(msg.author).child("balance").get()
            await client.send_message(msg.channel, "Your balance is " + str(
                dbfunctions.get_balance(msg.author)) + " <:chumcoin:337841443907305473>")

    # Takes money from the message author's balance
    # and places it in the balance of the user specified in
    # the first command argument.
    elif msg.content.startswith(".pay"):
        if not dbfunctions.is_registered(msg.author):
            await client.send_message(msg.channel, "You need to use **.register** first " + msg.author.mention + "!")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .pay <user> <amount>")
            elif functions.is_valid_userid(args[1]) is None:
                await client.send_message(msg.channel, "That doesn't look like a username.")
            elif not dbfunctions.is_registered(re.sub("[^0-9]", "", args[1])):  # TODO Fix this!
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
                elif payee == msg.author:
                    await client.send_message(msg.channel, "You can't pay yourself!")
                elif not dbfunctions.check_for_funds(msg.author, amt):
                    await client.send_message(msg.channel, "Sorry, you don't have enough chumcoins for that!")
                elif amt <= 0:
                    await client.send_message(msg.channel, "You can only pay amounts above 0")
                else:
                    await client.send_message(msg.channel,
                                              "" + msg.author.mention + "  :arrow_right:  "
                                              + "<:chumcoin:337841443907305473> x"
                                              + args[2] + "  :arrow_right:  " + args[1])

                    dbfunctions.withdraw(msg.author, amt)
                    dbfunctions.deposit(payee, amt)

    # Adds money to the balance of the user specified
    # in the first command argument. Only usable by users
    # with admin rank.
    elif msg.content.startswith(".give"):
        if not functions.user_is_admin(msg.author):
            await client.send_message(msg.channel, "You must be an admin to use .give")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .give <user> <amount>")
            elif functions.is_valid_userid(args[1]) is None:
                await client.send_message(msg.channel, "That doesn't look like a username.")
            elif not dbfunctions.is_registered(re.sub("[^0-9]", "", args[1])):  # TODO This too!
                await client.send_message(msg.channel, "That user isn't registered!")
            else:
                payee = re.sub("[^0-9]", "", args[1])
                try:
                    amt = int(args[2])
                except:
                    # TODO Move this up
                    await client.send_message(msg.channel, "You can only give amounts that are whole numbers")
                    amt = -1

                if amt == -1:
                    # amt wasn't an int, do nothing
                    print()
                else:
                    await client.send_message(msg.channel,
                                              "<:chumcoin:337841443907305473> x" + args[2] + "  :arrow_right:  " + args[
                                                  1])
                    dbfunctions.deposit(payee, amt)

    # Takes money from the balance of the user specified
    # in the first command argument. Only usable by users
    # with admin rank.
    elif msg.content.startswith(".take"):
        if not functions.user_is_admin(msg.author):
            await client.send_message(msg.channel, "You must be an admin to use .take")
        else:
            args = str.split(msg.content)

            if len(args) != 3:
                await client.send_message(msg.channel, "Usage: .take <user> <amount>")
            elif functions.is_valid_userid(args[1]) is None:
                await client.send_message(msg.channel, "That doesn't look like a username.")
            elif not dbfunctions.is_registered(re.sub("[^0-9]", "", args[1])):  # TODO This too!
                await client.send_message(msg.channel, "That user isn't registered!")
            else:
                payee = re.sub("[^0-9]", "", args[1])
                try:
                    amt = int(args[2])
                except:
                    # TODO Move this up
                    await client.send_message(msg.channel, "You can take give amounts that are whole numbers")
                    amt = -1

                if amt == -1:
                    # amt wasn't an int, do nothing
                    print()
                else:
                    await client.send_message(msg.channel, "" + args[1]
                                              + "  :arrow_right:  <:chumcoin:337841443907305473> x" + args[2])
                    dbfunctions.withdraw(payee, amt)

    # Force-sets a user's "isInDeal" status to false.
    # Intended to be used if this status gets stuck
    # when the bot disconnects while a user in in a deal.
    # Using this while a user in in a deal and the bot
    # is still online will still allow the deal to be
    # completeed, and will also allow a user to be
    # in multiple deals at once. If no user is specified
    # the command affects the user.
    elif msg.content.startswith(".forceenddeal"):
        if not functions.user_is_admin(msg.author):
            await client.send_message(msg.channel, "You must be an admin to use .forceenddeal")
        else:
            args = str.split(msg.content)

            if len(args) > 2:
                await client.send_message(msg.channel, "Usage: .forceenddeal [user]")
            elif len(args) == 2:
                dbfunctions.set_deal_status(re.sub("[^0-9]", "", args[1]), False)
                await client.send_message(msg.channel, "Ended deal for " + args[1])
            else:
                dbfunctions.set_deal_status(msg.author.id, False)
                await client.send_message(msg.channel, "Ended deal for " + msg.author.mention)

    # Deletes the "lastDealTime" key for a user. If
    # no user is specified the command affects the
    # issuer.
    elif msg.content.startswith(".forceendcooldown"):
        if not functions.user_is_admin(msg.author):
            await client.send_message(msg.channel, "You must be an admin to use .forceendcooldown")
        else:
            args = str.split(msg.content)

            if len(args) > 2:
                await client.send_message(msg.channel, "Usage: .forceendcooldown [user]")
            elif len(args) == 2:
                db.child("users").child(re.sub("[^0-9]", "", args[1])).child("lastDealTime").remove()
                await client.send_message(msg.channel, "Ended cooldown for " + args[1])
            else:
                db.child("users").child(msg.author.id).child("lastDealTime").remove()
                await client.send_message(msg.channel, "Ended cooldown for " + msg.author.mention)

    # Starts an appraisal of a string or an attachment.
    # Based on random.random() a value is assigned and offered
    # to the author of the message. Also checks to make sure the
    # author does not already have and active appraisal, and that
    # they have not made a deal within the appraisal cooldown time.
    elif msg.content.startswith(".appraise"):
        now = int(time.time())

        if not dbfunctions.is_registered(msg.author):
            await client.send_message(msg.channel, "You need to use **.register** first " + msg.author.mention + "!")
        elif dbfunctions.is_in_deal(msg.author):
            await client.send_message(msg.channel,
                                      "Looks like you've already got a deal on the table " + msg.author.mention + "!")
        elif dbfunctions.last_deal_time(msg.author) is not None and not functions.in_cooldown_period(msg.author):

            secondstonextdeal = 900 - (now - dbfunctions.last_deal_time(msg.author))
            if secondstonextdeal <= 60:
                timetodealstring = "" + str(int(round(secondstonextdeal, 0))) + " more seconds"
            else:
                timetodealstring = "" + str(int(round(secondstonextdeal / 60, 0))) + " more minutes"

            await client.send_message(msg.channel, "You've gotta wait " + timetodealstring
                                      + " until your next deal " + msg.author.mention + ".")
        else:
            seller = msg.author
            dbfunctions.set_deal_status(seller, True)

            args = str.split(msg.content)
            files = msg.attachments

            random.seed()
            base = random.random()

            value = functions.calc_appraisal_value(base)
            quote = functions.get_appraisal_quote(base)

            if len(args) == 1 and len(files) == 0:
                await client.send_message(msg.channel, "You must include something to appraise")
                dbfunctions.set_deal_status(seller, False)
            else:
                if not value == 0:
                    await client.send_message(msg.channel, quote + "\n\n" + msg.author.mention + " Offer: "
                                              + str(value) + " <:chumcoin:337841443907305473> (.deal/.nodeal)")

                    def check(i):
                        return i.content == ".deal" or i.content == ".nodeal"

                    response = await client.wait_for_message(timeout=30.0, author=msg.author, check=check)

                    if response is None:
                        await client.send_message(msg.channel, "Alright, no deal then.")
                        dbfunctions.set_deal_status(seller, False)
                    elif response.content == ".deal":
                        await client.send_message(msg.channel,
                                                  "Alright! I'll meet you over there and do some paperwork.")
                        await client.send_message(msg.channel,
                                                  "<:chumlee:337842115931537408>  :arrow_right:  "
                                                  "<:chumcoin:337841443907305473> x" + str(
                                                      value) + "  :arrow_right:  " + msg.author.mention)
                        dbfunctions.deposit(msg.author, value)
                        dbfunctions.set_deal_status(seller, False)
                        dbfunctions.update_last_deal_time(seller)
                    elif response.content == ".nodeal":
                        await client.send_message(msg.channel, "Alright, no deal then.")
                        dbfunctions.set_deal_status(seller, False)
                    else:
                        await client.send_message(msg.channel, "Something went wrong!")
                        dbfunctions.set_deal_status(seller, False)
                else:
                    await client.send_message(msg.channel, quote + "\n\nNo deal :no_entry_sign:")
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
        # medals = db.child("users").child(msg.author).child("medals").order_by_value().equal_to(True).get()
        medals = dbfunctions.get_medals(msg.author)
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
            await client.send_message(msg.channel, functions.buy_medal(msg.author, args[1]))


# Run the bot
client.run("MzM4NDIxOTMyNDI2OTE5OTM2.DFVLkA.oH1RXMJFxlFqi2BPgTwcUGKRiFs")
