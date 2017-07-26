import re
import time

import dbfunctions
import resources.medalprices

medalprices = resources.medalprices

dealcooldown = 900


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
