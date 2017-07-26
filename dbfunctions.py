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
        user = user.id

    currentbalance = db.child("users").child(user).child("balance").get()
    newbalance = currentbalance.val() + amt
    db.child("users").child(user).child("balance").set(newbalance)


def withdraw(user, amt):
    if hasattr(user, "id"):
        user = user.id

    currentbalance = db.child("users").child(user).child("balance").get()
    newbalance = currentbalance.val() - amt
    db.child("users").child(user).child("balance").set(newbalance)


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

    return db.child("users").child(user).child("medals").order_by_value().equal_to(True).get().val()
