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


def get_cooldown_multiplier(user: discord.User):
    multiplier = db.reference(f"{db_root}/cooldowns/{user.id}/multiplier").get()
    if multiplier is None:
        return 1
    else:
        return multiplier


def increase_cooldown_multiplier(user: discord.User):
    current_multiplier = get_cooldown_multiplier(user)
    if current_multiplier != MAX_COOLDOWN_MULTIPLIER:
        db.reference(f"{db_root}/cooldowns/{user.id}/multiplier").set(current_multiplier * 1.5)


def decrease_cooldown_multiplier(user: discord.User):
    current_multiplier = get_cooldown_multiplier(user)
    if current_multiplier != BASE_COOLDOWN_MULTIPLIER:
        db.reference(f"{db_root}/cooldowns/{user.id}/multiplier").set(current_multiplier / 1.5)


def update_cooldown_end_time(user: discord.User, appraisal_time: int):
    last_cooldown_end_time = get_cooldown_end_time(user)

    if last_cooldown_end_time is None:
        db.reference(f"{db_root}/cooldowns/{user.id}/cooldownEnd").set(int(time.time()) + BASE_COOLDOWN_PERIOD_SECONDS)
    else:
        time_since_cooldown_end = appraisal_time - last_cooldown_end_time

        # If within 5 minutes of last cooldown expiring increase the next cooldown
        # If between 5 and 10 minutes leave it the same
        # If more than 10 decrease it
        if time_since_cooldown_end <= 300:
            increase_cooldown_multiplier(user)
        elif time_since_cooldown_end > 600:
            decrease_cooldown_multiplier(user)

        cooldown_multiplier = get_cooldown_multiplier(user)
        cooldown_length = BASE_COOLDOWN_PERIOD_SECONDS * cooldown_multiplier

        db.reference(f"{db_root}/cooldowns/{user.id}/cooldownEnd").set(int(time.time()) + cooldown_length)


BASE_COOLDOWN_PERIOD_SECONDS = 300
BASE_COOLDOWN_MULTIPLIER = 1
MAX_COOLDOWN_MULTIPLIER = 3.375
