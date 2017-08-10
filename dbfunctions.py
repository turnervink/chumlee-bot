import time

from resources.firebaseinfo import db

cooldowntime = 900
patiencerange = 300


def is_registered(user):
    """
    Checks if a user is registered in the database.

    :param user: the user ID string or User object to check
    :return: True if the user is registered
    """
    if hasattr(user, "id"):
        user = user.id

    dbusername = db.child("users").child(user).get()

    if dbusername.val() is None:
        return False
    else:
        return True


def get_balance(user):
    """
    Gets a user's coin balance.

    :param user: the user ID string or User object to get the balance for
    :return: the user's balance as an int
    """
    if hasattr(user, "id"):
        user = user.id

    return db.child("users").child(user).child("balance").get().val()


def deposit(user, amt):
    """
    Deposits coins into a user's account.

    :param user: the user ID string or User object to give funds to
    :param amt: the amount of funds to give
    :return: a string containing a success/failure message to be sent to the
    Discord channel where the command was issued
    """
    if hasattr(user, "id"):
        mention = user.mention
        user = user.id
    else:
        mention = "<@" + user + ">"

    try:
        amt = int(amt)
    except ValueError:
        return "You can only give amounts that are whole numbers " + mention + "!"

    balance = db.child("users").child(user).child("balance").get().val()

    if amt <= 0:
        return "Can't deposit a negative/zerp amount into " + mention + "'s account!"
    else:
        db.child("users").child(user).child("balance").set(balance + amt)
        return "<:chumcoin:337841443907305473> x" + str(amt) + "  :arrow_right:  " + mention


def withdraw(user, amt):
    """
    Withdraws coins from a user's account. Checks to make sure the user has sufficient funds.

    :param user: the user ID string or User object to withdraw funds from
    :param amt: the amount of funds to withdraw
    :return: a string containing a success/failure message to be sent to the
    Discord channel where the command was issued
    """
    if hasattr(user, "id"):
        mention = user.mention
        user = user.id
    else:
        mention = "<@" + user + ">"

    try:
        amt = int(amt)
    except ValueError:
        return "You can only take amounts that are whole numbers " + mention + "!"

    balance = db.child("users").child(user).child("balance").get().val()

    if amt <= 0:
        return "Can't take a negative/zero amount from " + mention + "'s account!"
    elif amt > balance:
        return "That's more than " + mention + "'s account has!"
    else:
        db.child("users").child(user).child("balance").set(balance - amt)
        return "<@" + user + ">  :arrow_right:  <:chumcoin:337841443907305473> x" + str(amt)


def transfer(payer, payee, amt):
    """
    Transfers funds from one user's account to another.

    :param payer: the user ID string or User object to withdraw funds from
    :param payee: the user ID string or User object to give funds to
    :param amt: the amount of funds to transer
    :return:
    """
    if hasattr(payer, "id"):
        payermention = payer.mention
        payer = payer.id
    else:
        payermention = "<@" + payer + ">"

    if hasattr(payee, "id"):
        payeemention = payee.mention
        payee = payee.id
    else:
        payeemention = "<@" + payee + ">"

    try:
        amt = int(amt)
    except ValueError:
        return "You can only pay amounts that are whole numbers " + payermention + "!"

    payerbalance = db.child("users").child(payer).child("balance").get().val()

    if payer == payee:
        return "You can't pay yourself " + payermention + "!"
    elif amt <= 0:
        return "You can only pay amounts above 0 " + payermention + "!"
    elif amt > payerbalance:
        return "You don't have enough Chumcoins " + payermention + "!"
    else:
        withdraw(payer, amt)
        deposit(payee, amt)
        return "" + payermention + "  :arrow_right:  " + "<:chumcoin:337841443907305473> x" \
               + str(amt) + "  :arrow_right:  " + payeemention


def check_for_funds(user, amt):
    """
    Checks if a user has sufficient funds for a given amount.

    :param user: the user ID string or User object to check the funds of
    :param amt: the amount of funds to check for
    :return: True if the user has sufficient funds
    """
    if hasattr(user, "id"):
        user = user.id

    currentbalance = db.child("users").child(user).child("balance").get().val();
    return currentbalance >= amt


def set_deal_status(user, status):
    """
    Sets the deal status of a user.

    :param user: the user ID string or User object to set the status for
    :param status: the status to set. True indicates the user is in a deal
    """
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("isInDeal").set(status)


def is_in_deal(user):
    """
    Checks the deal status of a user.

    :param user: the user ID string or User object to check the status of
    :return: True if the user is in a deal
    """
    if hasattr(user, "id"):
        user = user.id

    return db.child("users").child(user).child("isInDeal").get().val()


def get_cooldown_end_time(user):
    """
    Gets the timestamp for the end time of a user's cooldown.

    :param user: the user ID string or User object to get the cooldown end of
    :return: a Unix timestamp of the end time for the user's cooldown
    """
    if hasattr(user, "id"):
        user = user.id

    return db.child("cooldowns").child(user).child("cooldownEnd").get().val()


def get_remaining_cooldown_time(user):
    """
    Gets the remaining amount of time in a user's cooldown.

    :param user: the user ID string or User object to get the time remaining of
    :return: the remaining time in seconds
    """
    if hasattr(user, "id"):
        user = user.id

    try:
        return db.child("cooldowns").child(user).child("cooldownEnd").get().val() - int(time.time())
    except ValueError:
        print("Error calculating time left in cooldown!")
        return None


def update_cooldown_end(user):
    """
    Gets the current time and adds the cooldown length to it. Stores the result at cooldowns/user/cooldownEnd in the
    database.

    :param user: the user ID string or User object to set the cooldown end for
    """
    if hasattr(user, "id"):
        user = user.id

        now = int(time.time())
        print("Base end time: " + (str(now + cooldowntime)))
        multiplier = db.child("cooldowns").child(user).child("multiplier").get().val()
        print("Mult: " + str(multiplier))

        try:
            db.child("cooldowns").child(user).child("cooldownEnd").set(now + (cooldowntime * multiplier))
        except ValueError:
            print("Mult error!")
            db.child("cooldowns").child(user).child("cooldownEnd").set(now + cooldowntime)


def update_last_nodeal_time(user):
    if hasattr(user, "id"):
        user = user.id

    db.child("cooldowns").child(user).child("lastDealRejection").set(int(time.time()))


def get_last_deal_time(user):
    if hasattr(user, "id"):
        user = user.id

    return db.child("cooldowns").child(user).child("lastDealRejection").get().val()


def get_cooldown_multiplier(user):
    """
    Currently unused. Gets the current cooldown time multiplier for a user.

    :param user: the user ID string or User object to get the multiplier of
    :return: the current multiplier
    """
    if hasattr(user, "id"):
        user = user.id

    print("Got mult: " + str(db.child("cooldowns").child(user).child("multiplier").get().val()))

    return db.child("cooldowns").child(user).child("multiplier").get().val()


def adjust_cooldown_multiplier(user, dealstarttime):
    """
    Determines whether to increase or decrease a user's cooldown multiplier based on how long they have waited between
    making deals. If a user has waited longer than the "patience time" the multiplier is reduced by 0.1, otherwise it
    is increased by 0.1. If the multiplier is already at 1.0 it will not be reduced further.

    :param user: the user ID string or User object to adjust the multiplier for
    :param dealstarttime: the time the current deal was started as a Unix timestamp
    """
    print("Adjusting mult")
    if hasattr(user, "id"):
        user = user.id

    cooldownend = get_cooldown_end_time(user)
    print("End: " + str(cooldownend))
    if cooldownend is not None:
        print("There is an end time!")
        currentmultiplier = db.child("cooldowns").child(user).child("multiplier").get().val()
        if currentmultiplier is None:
            currentmultiplier = 1.0
            db.child("cooldowns").child(user).child("multiplier").set(currentmultiplier)

        if dealstarttime - cooldownend > patiencerange:
            if not currentmultiplier == 1.0:
                print("Decreasing cooldown")
                db.child("cooldowns").child(user).child("multiplier").set(round(currentmultiplier - 0.1, 1))
            else:
                print("Leaving mult at 1.0")
        else:
            print("Increasing cooldown")
            db.child("cooldowns").child(user).child("multiplier").set(round(currentmultiplier + 0.1, 1))


def award_medal(user, medal):
    """
    Awards a medal to a user.

    :param user: the user ID string or User object to award the medal to
    :param medal: the medal to award
    """
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("medals").child(medal).set(True)


def take_medal(user, medal):
    """
    Takes a medal from a user.

    :param user: the user ID string or User object to take the medal from
    :param medal: the medal to take
    """
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("medals").child(medal).set(False)


def get_medals(user):
    """
    Gets all of the medals a user has aquired.

    :param user: the user ID string or User object to get the medals of
    :return: the user's medals as a dict
    """
    if hasattr(user, "id"):
        user = user.id

    try:
        medals = db.child("users").child(user).child("medals").order_by_value().equal_to(True).get().val()
    except IndexError:
        return None

    return medals


def update_lotto_status(server, state):
    db.child("lotteries").child(server.id).child("lottoInProgress").set(state)


def get_lotto_status(server):
    return db.child("lotteries").child(server.id).child("lottoInProgress").get().val()


def update_deal_attempts(user):
    if hasattr(user, "id"):
        user = user.id

    if get_last_deal_time(user) is not None and int(time.time()) - get_last_deal_time(user) <= cooldowntime:
        attempts = db.child("cooldowns").child(user).child("dealAttempts").get().val()

        if attempts is None:
            attempts = 1
        else:
            attempts = attempts + 1

        db.child("cooldowns").child(user).child("dealAttempts").set(attempts)
    else:
        db.child("cooldowns").child(user).child("dealAttempts").set(1)


def reset_deal_attempts(user):
    if hasattr(user, "id"):
        user = user.id

    db.child("cooldowns").child(user).child("dealAttempts").set(0)


def get_deal_attempts(user):
    if hasattr(user, "id"):
        user = user.id

    return db.child("cooldowns").child(user).child("dealAttempts").get().val()