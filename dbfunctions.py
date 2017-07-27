from resources.firebaseinfo import db
import time


def is_registered(user):
    if hasattr(user, "id"):
        user = user.id

    dbusername = db.child("users").child(user).get()

    if dbusername.val() is None:
        return False
    else:
        return True


def get_balance(user):
    if hasattr(user, "id"):
        user = user.id

    return db.child("users").child(user).child("balance").get().val()


def deposit(user, amt):
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
    if hasattr(user, "id"):
        user = user.id

    currentbalance = db.child("users").child(user).child("balance").get().val();
    return currentbalance >= amt


def set_deal_status(user, status):
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("isInDeal").set(status)


def is_in_deal(user):
    if hasattr(user, "id"):
        user = user.id

    return db.child("users").child(user).child("isInDeal").get().val()


def update_last_deal_time(user):
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("lastDealTime").set(int(time.time()))


def last_deal_time(user):
    if hasattr(user, "id"):
        user = user.id

    return db.child("users").child(user).child("lastDealTime").get().val()


def award_medal(user, medal):
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("medals").child(medal).set(True)


def take_medal(user, medal):
    if hasattr(user, "id"):
        user = user.id

    db.child("users").child(user).child("medals").child(medal).set(False)


def get_medals(user):
    if hasattr(user, "id"):
        user = user.id

    try:
        medals = db.child("users").child(user).child("medals").order_by_value().equal_to(True).get().val()
    except IndexError:
        return None

    return medals
