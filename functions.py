import re
import time
import random

import dbfunctions
import resources.medalprices
import resources.prawnsrars
prawnsrars = resources.prawnsrars

medalprices = resources.medalprices

dealcooldown = 900
tier1 = 0.1
tier2 = 0.25
tier3 = 0.5
tier4 = 0.75
tier5 = 0.95


def user_is_admin(user):
    return str(user.top_role) == "admin"

def is_valid_userid(user):
    if hasattr(user, "id"):
        user = user.id

    return re.match("<@!?[0-9]*>", user)


def in_cooldown_period(user):
    if hasattr(user, "id"):
        user = user.id

    now = int(time.time())
    lastdeal = dbfunctions.last_deal_time(user)

    return (now - lastdeal) >= dealcooldown


def calc_appraisal_value(base):
    if base > tier5:
        return random.randint(500, 1000)
    elif base > tier4:
        return random.randint(250, 500)
    elif base > tier3:
        return random.randint(100, 250)
    elif base > tier2:
        return random.randint(10, 100)
    elif base > tier1:
        return random.randint(1, 10)
    else:
        return 0


def get_appraisal_quote(val):
    if val > tier5:
        return random.choice(prawnsrars.tier5)
    elif val > tier4:
        return random.choice(prawnsrars.tier4)
    elif val > tier3:
        return random.choice(prawnsrars.tier3)
    elif val > tier2:
        return random.choice(prawnsrars.tier2)
    elif val > tier1:
        return random.choice(prawnsrars.tier1)
    else:
        return random.choice(prawnsrars.tier0)


def buy_medal(user, medal):
    medal = str.lower(medal)
    price = medalprices.get_medal_price(medal)
    if price is None:
        return "There isn't a medal called " + medal + "."
    elif medal in dbfunctions.get_medals(user.id):
        return "You already have the " + medal + " medal " + user.mention + "!"
    else:
        if dbfunctions.check_for_funds(user.id, price):
            dbfunctions.withdraw(user.id, price)
            dbfunctions.award_medal(user.id, medal)
            return "Alright! Here's a " + medal + " medal for you " + user.mention + "!\n\n" \
                + user.mention + ":arrow_right:  <:chumcoin:337841443907305473> x" \
                + str(medalprices.get_medal_price(medal)) + "  :arrow_right:  <:chumlee:337842115931537408>"
        else:
            return "You don't have enough Chumcoins for a " + medal + " medal!"
