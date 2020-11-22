from .config import db
import discord

import time


def get_cooldown_end_time(user: discord.User):
    return db.child("cooldowns").child(user.id).child("cooldownEnd").get().val()


def update_cooldown_end_time(user: discord.User):
    db.child("cooldowns").child(user.id).child("cooldownEnd").set(int(time.time()) + COOLDOWN_PERIOD_SECONDS)


COOLDOWN_PERIOD_SECONDS = 900
