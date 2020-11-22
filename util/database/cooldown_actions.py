from .config import db
import discord

import time


def get_cooldown_end_time(user: discord.User):
    return db.child("cooldowns").child(user.id).child("cooldownEnd").get().val()


def update_cooldown_end_time(user: discord.User):
    """
    Update the cooldown time for a user to be COOLDOWN_PERIOD_SECONDS in the future.
    :param user: the user to update the cooldown for
    """
    db.child("cooldowns").child(user.id).child("cooldownEnd").set(int(time.time()) + COOLDOWN_PERIOD_SECONDS)


def get_rejected_offer_count(user: discord.User):
    rejected_offer_count = db.child("cooldowns").child(user.id).child("rejectedOffers").get().val()
    if rejected_offer_count is not None:
        return rejected_offer_count
    else:
        return 0


def inc_rejected_offer_count(user: discord.User):
    rejected_offer_count = get_rejected_offer_count(user)
    db.child("cooldowns").child(user.id).child("rejectedOffers").set(rejected_offer_count + 1)


def get_last_rejected_offer_time(user: discord.User):
    return db.child("cooldowns").child(user.id).child("lastRejectedOfferTime").get().val()


def set_last_rejected_offer_time(user: discord.User):
    db.child("cooldowns").child(user.id).child("lastRejectedOfferTime").set(int(time.time()))


COOLDOWN_PERIOD_SECONDS = 900
