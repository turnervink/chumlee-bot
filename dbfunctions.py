from resources.firebaseinfo import db
import time


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


def update_last_deal_time(user):
    """
    Updates a user's last deal time to the current time.

    :param user: the user ID string or User object to update the time for
    """
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("lastDealTime").set(int(time.time()))


def last_deal_time(user):
    """
    Get's the time of a user's last deal.

    :param user: the user ID string or User object to get the last deal time of
    :return: unix timestamp as an int
    """
    if hasattr(user, "id"):
        user = user.id

    return db.child("users").child(user).child("lastDealTime").get().val()


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
