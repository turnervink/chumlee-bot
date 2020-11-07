import discord
import re
import random
import json
import time
import io
import os

import functions
import dbfunctions
import profile
from resources.firebaseinfo import db
import resources.prawnsrars
import resources.medals

medals = resources.medals

client = discord.Client()

allowedchannels = ["bot-testing", "the-pawnshop"]  # Names of channels where bot commands can be used
globalcommands = [".help", ".commands"]  # Commands that can be used in any channel

# List of all commands to determine when the bot should start typing
commands = [
    ".help",
    ".commands",
    ".register",
    ".balance",
    ".pay",
    ".give",
    ".take",
    ".forceenddeal",
    ".forceendcooldown",
    ".appraise",
    ".cooldown",
    ".kevincostner",
    ".item",
    ".purge",
    ".listmedals",
    ".medals",
    ".mymedals",
    ".profile",
    ".buymedal",
    ".lotto"
    # ".gif"
]


@client.event
async def on_ready():
    """
    Called when the bot successfully connects.
    """
    print("-----")
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print("-----")


@client.event
async def on_message(msg):
    """
    Called whenever a message is sent to somewhere the bot is connected.

    :param msg: a Message object representing the message that was sent
    """
    # Check if a message starts with a valid command. If so, show a typing indicator and ensure the command was issued
    # in an allowed place.
    if len(str.split(msg.content)) > 0 and str.split(msg.content)[0] in commands:
        if str.split(msg.content)[0] not in globalcommands \
                and msg.guild is not None \
                and str(msg.channel) not in allowedchannels:

            await msg.channel.send("Only **#the-pawnshop** can be used for chumlee-bot commands!")
        else:
            if dbfunctions.is_registered(msg.author):
                # Update user info in Firebase
                dbfunctions.update_user_metadata(msg.author)

            # Displays a help/welcome message to get users started.
            if msg.content.startswith(".help"):
                welcomemsg = ("Hi! I'm Chumlee, and I run this pawn shop. To get started, "
                              "use **.register** to register yourself in the database. "
                              "Then use **.commands** to see what I can do!  If you "
                              "haven't already, set up a channel called **#the-pawnshop** "
                              "so you can interact with me!"
                              "\n\n"
                              "By having me in your server, you're agreeing to the terms of service "
                              "which can be found here https://sites.google.com/view/chumlee-bot-tos/home")
                await msg.channel.send(welcomemsg)

            # Displays available commands and their uses.
            elif msg.content.startswith(".commands"):
                commandinfo = ("*Commands*:\n"
                               "**.register:** register in the <:chumcoin:337841443907305473> database\n\n"
                               "**.balance [@user]:** check your or another user's "
                               "<:chumcoin:337841443907305473> balance\n\n"
                               "**.appraise <text/attachment>:** get an appraisal for an item\n\n"
                               "**.pay <@user> <amount>:** pay someone <:chumcoin:337841443907305473>s\n\n"
                               "**.profile:** see your Chumprofile\n\n"
                               "**.medals:** see available Chummedals\n\n"
                               "**.buymedal <medal>:** buy a Chummedal\n\n"
                               "**.cooldown:** check how long you still need to wait until your next deal\n\n"
                               "**.item:** gets a random item from the _Pawn Stars: The Game_ Wiki\n\n"
                               "**.purge:** delete the last 100 commands and bot messages\n\n"
                               "**.kevincostner:** dances with swolves\n\n"

                               "\n*Admin Commands:*\n"
                               "**.give <@user> <amount>:** (admin command) give a user "
                               "<:chumcoin:337841443907305473>s\n\n"
                               "**.take <@user> <amount>:** (admin command) take a user's "
                               "<:chumcoin:337841443907305473>s\n\n"
                               "**.forceenddeal [@user]:** set your or another user's deal status to false\n\n"
                               "**.forceendcooldown [@user]:** end your or another user's deal cooldown"
                               )
                await msg.author.send(commandinfo)
                await msg.channel.send("Command info sent!")

            # Registers a user in the database by adding their user ID to the "users" node and setting an initial
            # balance and value for "isInDeal".
            elif msg.content.startswith(".register"):
                if not dbfunctions.is_registered(msg.author):
                    newuserdata = {
                        "userName": msg.author.name,
                        "discriminator": msg.author.discriminator,
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

                    newcooldowndata = {
                        "multiplier": 1.0
                    }

                    db.child("users").child(msg.author.id).set(newuserdata)
                    db.child("cooldowns").child(msg.author.id).set(newcooldowndata)
                    await msg.channel.send("Okay, you're all set up " + msg.author.mention + "!")
                else:
                    await msg.channel.send("Looks like you're already registered "
                                           + msg.author.mention + ".")

            # Gets a user's balance from the database and prints it in the chat.
            elif msg.content.startswith(".balance"):
                args = str.split(msg.content)

                if not dbfunctions.is_registered(msg.author):
                    await msg.channel.send("You need to use **.register** first "
                                           + msg.author.mention + "!")
                elif len(args) == 2:
                    if not functions.user_is_admin(msg.author):
                        await msg.channel.send("You must be an admin to get the balance "
                                               "of another user.")
                    elif not functions.is_valid_userid(args[1]):
                        await msg.channel.send("That doesn't look like a username.")
                    elif not dbfunctions.is_registered(re.sub('[^0-9]', "", args[1])):
                        await msg.channel.send("That user isn't registered!")
                    else:
                        await msg.author.send(args[1] + "'s balance is " + str(
                            dbfunctions.get_balance(re.sub('[^0-9]', "", args[1]))) + " <:chumcoin:337841443907305473>")
                else:
                    await msg.channel.send(msg.author.mention + "'s balance is " + str(
                        dbfunctions.get_balance(msg.author)) + " <:chumcoin:337841443907305473>")

            # Transfers money between users.
            elif msg.content.startswith(".pay"):
                if not dbfunctions.is_registered(msg.author):
                    await msg.channel.send("You need to use **.register** first "
                                           + msg.author.mention + "!")
                else:

                    args = str.split(msg.content)

                    if len(args) != 3:
                        await msg.channel.send("Usage: .pay <user> <amount>")
                    elif functions.is_valid_userid(args[1]) is None:
                        await msg.channel.send("That doesn't look like a username.")
                    elif not dbfunctions.is_registered(re.sub('[^0-9]', "", args[1])):
                        await msg.channel.send("That user isn't registered!")
                    else:
                        await msg.channel.send(dbfunctions.transfer(msg.author,
                                                                    re.sub('[^0-9]', "",
                                                                           args[1]), args[2]))

            # Adds money to the balance of the user specified in the first command argument. Only usable by users
            # with admin rank.
            elif msg.content.startswith(".give"):
                if not functions.user_is_admin(msg.author):
                    await msg.channel.send("You must be an admin to use .give")
                else:
                    args = str.split(msg.content)

                    if len(args) != 3:
                        await msg.channel.send("Usage: .give <user> <amount>")
                    elif functions.is_valid_userid(args[1]) is None:
                        await msg.channel.send("That doesn't look like a username.")
                    elif not dbfunctions.is_registered(re.sub('[^0-9]', "", args[1])):
                        await msg.channel.send("That user isn't registered!")
                    else:
                        await msg.channel.send(dbfunctions.deposit(re.sub('[^0-9]', "",
                                                                          args[1]), args[2]))

            # Takes money from the balance of the user specified in the first command argument. Only usable by users
            # with admin rank.
            elif msg.content.startswith(".take"):
                if not functions.user_is_admin(msg.author):
                    await msg.channel.send("You must be an admin to use .take")
                else:
                    args = str.split(msg.content)

                    if len(args) != 3:
                        await msg.channel.send("Usage: .take <user> <amount>")
                    elif functions.is_valid_userid(args[1]) is None:
                        await msg.channel.send("That doesn't look like a username.")
                    elif not dbfunctions.is_registered(re.sub('[^0-9]', "", args[1])):
                        await msg.channel.send("That user isn't registered!")
                    elif not dbfunctions.check_for_funds(re.sub('[^0-9]', "", args[1]), int(args[2])):
                        await msg.channel.send("That's more Chumcoins than that user has!")
                    else:
                        await msg.channel.send(dbfunctions.withdraw(re.sub('[^0-9]', "",
                                                                           args[1]), args[2]))

            # Force-sets a user's "isInDeal" status to false. Intended to be used if this status gets stuck
            # when the bot disconnects while a user in in a deal. Using this while a user in in a deal and the bot
            # is still online will still allow the deal to be completeed, and will also allow a user to be
            # in multiple deals at once. If no user is specified the command affects the issuer. Only usable by users
            # with admin rank.
            elif msg.content.startswith(".forceenddeal"):
                if not functions.user_is_admin(msg.author):
                    await msg.channel.send("You must be an admin to use .forceenddeal")
                else:
                    args = str.split(msg.content)

                    if len(args) > 2:
                        await msg.channel.send("Usage: .forceenddeal [user]")
                    elif len(args) == 2:
                        dbfunctions.set_deal_status(re.sub('[^0-9]', "", args[1]), False)
                        await msg.channel.send("Ended deal for " + args[1])
                    else:
                        dbfunctions.set_deal_status(msg.author.id, False)
                        await msg.channel.send("Ended deal for " + msg.author.mention)

            # Deletes the "lastDealTime" key for a user. If no user is specified the command affects the issuer.
            # Only usable by users with admin rank.
            elif msg.content.startswith(".forceendcooldown"):
                if not functions.user_is_admin(msg.author):
                    await msg.channel.send("You must be an admin to use .forceendcooldown")
                else:
                    args = str.split(msg.content)

                    if len(args) > 2:
                        await msg.channel.send("Usage: .forceendcooldown [user]")
                    elif len(args) == 2:
                        db.child("cooldowns").child(re.sub('[^0-9]', "", args[1])).child("cooldownEnd").remove()
                        await msg.channel.send("Ended cooldown for " + args[1])
                    else:
                        db.child("cooldowns").child(msg.author.id).child("cooldownEnd").remove()
                        await msg.channel.send("Ended cooldown for " + msg.author.mention)

            # Starts an appraisal of a string or an attachment.
            elif msg.content.startswith(".appraise"):

                if not dbfunctions.is_registered(msg.author):

                    await msg.channel.send("You need to use **.register** first "
                                           + msg.author.mention + "!")
                elif dbfunctions.is_in_deal(msg.author):
                    await msg.channel.send(
                        "Looks like you've already got a deal on the table "
                        + msg.author.mention + "!")
                elif not functions.cooldown_expired(msg.author):
                    secondstonextdeal = dbfunctions.get_remaining_cooldown_time(msg.author)
                    if secondstonextdeal <= 60:
                        timetodealstring = "" + str(int(round(secondstonextdeal, 0))) + " more seconds"
                    else:
                        timetodealstring = "" + str(int(round(secondstonextdeal / 60, 0))) + " more minutes"
                    await msg.channel.send("You've gotta wait " + timetodealstring
                                           + " until your next deal " + msg.author.mention + ".")
                # check if nodeal count is >= 3
                # if true, say you can't make a deal and start cooldown
                # reset count to 0
                elif dbfunctions.get_deal_attempts(msg.author) is not None \
                        and dbfunctions.get_deal_attempts(msg.author) >= 3:
                    await msg.channel.send(
                        "You've tried to make too many deals lately " + msg.author.mention
                        + "! Come back a bit later.")
                    dbfunctions.reset_deal_attempts(msg.author)
                    dbfunctions.update_cooldown_end(msg.author)
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
                        await msg.channel.send("You must include something to appraise")
                        dbfunctions.set_deal_status(seller, False)
                    elif len(args) > 1 and re.match('<@!?338421932426919936>', args[1]):
                        await msg.channel.send("I'll all about self love " + msg.author.mention
                                               + ", so I'll give myself a 10/10.")
                        dbfunctions.set_deal_status(msg.author, False)
                    else:
                        if not value == 0:
                            await msg.channel.send(quote + "\n\n" + msg.author.mention + " Offer: "
                                                   + str(value) + " <:chumcoin:337841443907305473> (.deal/.nodeal)")

                            def check(i):
                                return i.author == msg.author and i.content == ".deal" or i.content == ".nodeal"

                            response = await client.wait_for('message', timeout=60, check=check)

                            if response is None:
                                await msg.channel.send("Alright, no deal then.")

                                dbfunctions.set_deal_status(seller, False)
                                dbfunctions.update_cooldown_end(seller)

                            elif response.content == ".deal":
                                dbfunctions.adjust_cooldown_multiplier(seller, int(time.time()))

                                await msg.channel.send(
                                    "Alright! I'll meet you over there and do some paperwork.")
                                await msg.channel.send(
                                    "<:chumlee:337842115931537408>  :arrow_right:  "
                                    "<:chumcoin:337841443907305473> x" + str(
                                        value) + "  :arrow_right:  " + msg.author.mention)

                                dbfunctions.deposit(msg.author, value)
                                dbfunctions.set_deal_status(seller, False)
                                dbfunctions.reset_deal_attempts(seller)
                                dbfunctions.update_cooldown_end(seller)

                            elif response.content == ".nodeal":
                                await msg.channel.send("Alright, no deal then.")

                                dbfunctions.set_deal_status(seller, False)
                                # increment nodeal counter
                                dbfunctions.update_deal_attempts(seller)
                                dbfunctions.update_last_nodeal_time(seller)
                            else:
                                await msg.channel.send("Something went wrong!")

                                dbfunctions.set_deal_status(seller, False)

                        else:
                            await msg.channel.send(quote + "\n\nNo deal :no_entry_sign:")

                            dbfunctions.set_deal_status(seller, False)
                            dbfunctions.update_cooldown_end(seller)

            # Lets a user check how much longer they have to wait until making their next deal.
            elif msg.content.startswith(".cooldown"):
                if not dbfunctions.is_registered(msg.author):
                    await msg.channel.send("You need to use **.register** first "
                                           + msg.author.mention + "!")
                elif functions.cooldown_expired(msg.author):
                    await msg.channel.send("You're not in the cooldown period "
                                           + msg.author.mention + "!")
                else:
                    secondstonextdeal = dbfunctions.get_remaining_cooldown_time(msg.author)
                    if secondstonextdeal <= 60:
                        timetodealstring = "" + str(int(round(secondstonextdeal, 0))) + " more seconds"
                    else:
                        timetodealstring = "" + str(int(round(secondstonextdeal / 60, 0))) + " more minutes"

                    await msg.channel.send("You've gotta wait " + timetodealstring
                                           + " until your next deal " + msg.author.mention + ".")

            # Posts a link to DaThings1's "Prawn Srars" along with a random quote from the video.
            elif msg.content.startswith(".kevincostner"):
                await msg.channel.send(random.choice(resources.prawnsrars.ytpquotes))
                await msg.channel.send("https://www.youtube.com/watch?v=5mEJbX5pio8")

            # Posts a random item from the Pawn Stars: The Game wiki.
            elif msg.content.startswith(".item"):
                baseurl = "http://pawnstarsthegame.wikia.com"

                with open('resources/items.json') as data_file:
                    data = json.load(data_file)

                await msg.channel.send(baseurl + data[random.randint(0, len(data) - 1)]["value"])

            # Deletes chumlee-bot messages and issued commands sent in the last 100 messages.
            elif msg.content.startswith(".purge"):
                def check(i):
                    return i.author.id == client.user.id or i.content[:1] == "."

                try:
                    await msg.channel.purge(limit=100, check=check)
                    await msg.channel.send("Deleted last 100 commands and responses "
                                           ":put_litter_in_its_place:")
                except discord.errors.Forbidden:
                    await msg.channel.send("I need permission to manage messages "
                                           "in order to use .purge!")

            # Sends a list of the available Chummedals and their prices.
            elif msg.content.startswith(".medals") or msg.content.startswith(".listmedals"):
                await msg.channel.send(medals.medalinfo)

            # Lists a user's medals.
            elif msg.content.startswith(".mymedals") or msg.content.startswith(".profile"):
                if not dbfunctions.is_registered(msg.author):
                    await msg.channel.send("You need to use **.register** first "
                                           + msg.author.mention + "!")
                else:
                    await msg.channel.send(
                        file=discord.File(io.BytesIO(profile.gen_profile(msg.author)), filename="profile.png"))

            # Lets a user buy a Chummedal.
            elif msg.content.startswith(".buymedal"):
                args = str.split(msg.content)

                if not len(args) == 2:
                    await msg.channel.send("Usage: .buymedal <medal>")
                else:
                    await msg.channel.send(functions.buy_medal(msg.author, args[1]))

            elif msg.content.startswith(".lotto"):
                args = str.split(msg.content)

                if not dbfunctions.is_registered(msg.author):
                    await msg.channel.send("You need to use **.register** first "
                                           + msg.author.mention + "!")
                elif not len(args) == 2:
                    await msg.channel.send("Usage: .lotto <bet>")
                elif dbfunctions.get_lotto_status(msg.guild):
                    await msg.channel.send(
                        "Looks like a Chumlottery is already in progress on this server!")
                else:
                    dbfunctions.update_lotto_status(msg.guild, True)
                    bet = int(args[1])
                    jackpot = 0

                    await msg.channel.send(msg.author.mention
                                           + " has started a Chumlottery! Type **.bet** to bet "
                                           + str(bet) + " <:chumcoin:337841443907305473> and join!")

                    players = [msg.author]

                    def check(i):
                        if not i.author.id == msg.author.id \
                                and i.author not in players \
                                and dbfunctions.is_registered(i.author) \
                                and i.content == ".bet":
                            players.append(i.author)

                    response = await client.wait_for('message', timeout=60, check=check)

                    if response is None:
                        if len(players) > 1:
                            await msg.channel.send("Alright, no more bets!")

                            for user in players:
                                if not dbfunctions.check_for_funds(user, bet):
                                    await msg.channel.send(user.mention
                                                           + " doesn't have the Chumcoins to play the Chumlottery!")
                                    del players[user]
                                else:
                                    await msg.channel.send(dbfunctions.withdraw(user, bet))
                                    jackpot += bet

                            await msg.channel.send("Drawing a name... :slot_machine:")

                            winner = random.choice(players)

                            await msg.channel.send("Congrats " + winner.mention + "! You won "
                                                   + str(jackpot) + " <:chumcoin:337841443907305473>!")

                            await msg.channel.send(dbfunctions.deposit(winner, jackpot))
                            dbfunctions.update_lotto_status(msg.guild, False)

                        else:
                            await msg.channel.send("No registered users entered the Chumlottery!")

                            dbfunctions.update_lotto_status(msg.guild, False)

            # Sends a random gif from the resources/img/gifs directory (currently unused).
            elif msg.content.startswith(".gif"):
                gif = random.choice(os.listdir("resources/img/gifs"))
                await msg.channel.send(file=discord.File("resources/img/gifs/" + gif))


# Run the bot
client.run(os.environ["bot_token"])
