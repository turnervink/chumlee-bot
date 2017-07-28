import re
import time
import random

import dbfunctions
import resources.medals
import resources.prawnsrars
prawnsrars = resources.prawnsrars

medalprices = resources.medals

dealcooldown = 900
tier1 = 0.1
tier2 = 0.25
tier3 = 0.5
tier4 = 0.75
tier5 = 0.95


def user_is_admin(user):
    """
    Checks if a user has the top server role of "admin".

    :param user: the User object to check
    :return: True is the User has the admin role
    """
    return str(user.top_role) == "admin"


def is_valid_userid(user):
    """
    Checks if a user ID appears to be valid. Does not perform any server-side validation, only a regex check.

    :param user: the user ID string or User object to validate
    :return: True if valid user ID
    """
    if hasattr(user, "id"):
        user = user.id

    return re.match('<@!?[0-9]*>', user)


def in_cooldown_period(user):
    """
    Checks if a user is still within the deal cooldown period.

    :param user: the user ID string or User object to validate
    :return: True if the user is still within the cooldown period
    """
    if hasattr(user, "id"):
        user = user.id

    now = int(time.time())
    lastdeal = dbfunctions.last_deal_time(user)

    return (now - lastdeal) >= dealcooldown


def calc_appraisal_value(base):
    """
    Calculates a random coin value for an item.

    :param base: a random.random() value to use in
    calculating the item's value
    :return: the item's appraised value
    """
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
    """
    Gets a random dialogue quote from the correct tier based on the appraised value of an item.

    :param val: an item's appraised value
    :return: a dialogue quote string
    """
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
    """
    Lets a user purchase a medal. Checks that such a medal exists and that the user has sufficient funds.

    :param user: a User object representing the user purchasing the medal
    :param medal: the medal to purchase
    :return: a string containing a success/failure message to be sent to the
    Discord channel where the command was issued
    """
    print("buying medal")
    print(user)
    print(medal)
    medal = str.lower(medal)
    price = medalprices.get_medal_price(medal)
    print(price)
    dbfunctions.get_medals(user)

    if price is None:
        return "There isn't a medal called " + medal + "."
    elif dbfunctions.get_medals(user) is not None and medal in dbfunctions.get_medals(user):
        return "You already have the " + medal + " medal " + user.mention + "!"
    else:
        if dbfunctions.check_for_funds(user.id, price):
            dbfunctions.withdraw(user.id, price)
            dbfunctions.award_medal(user.id, medal)
            return "Alright! Here's a " + medal + " medal for you " + user.mention + "!\n\n  " \
                + user.mention + ":arrow_right:  <:chumcoin:337841443907305473> x" \
                + str(medalprices.get_medal_price(medal)) + "  :arrow_right:  <:chumlee:337842115931537408>"
        else:
            return "You don't have enough Chumcoins for a " + medal + " medal!"
