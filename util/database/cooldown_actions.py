from .config import db, db_root
import discord

import time


def get_cooldown_end_time(user: discord.User):
    return db.reference(f"{db_root}/cooldowns/{user.id}/cooldownEnd").get()


def get_remaining_cooldown_time(user: discord.User):
    try:
        cooldown_end_time = get_cooldown_end_time(user)
        now = int(time.time())
        if cooldown_end_time > now:
            return cooldown_end_time - now
        else:
            return None
    except ValueError:
        return None


def update_cooldown_end_time(user: discord.User):
    """
    Update the cooldown time for a user to be COOLDOWN_PERIOD_SECONDS in the future.
    :param user: the user to update the cooldown for
    """
    db.reference(f"{db_root}/cooldowns/{user.id}/cooldownEnd").set(int(time.time()) + COOLDOWN_PERIOD_SECONDS)


COOLDOWN_PERIOD_SECONDS = 900
