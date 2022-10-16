import time

import discord
from discord.ext import commands
from discord.ext.commands import BucketType

from error import errors
from util.database import user_actions, cooldown_actions


def user_registered():
    def predicate(ctx: discord.ApplicationContext):
        if user_actions.is_registered(ctx.author):
            return True
        else:
            raise errors.UserNotRegisteredError(ctx.author)
    return commands.check(predicate)


def user_not_registered():
    def predicate(ctx: discord.ApplicationContext):
        if not user_actions.is_registered(ctx.author):
            return True
        else:
            raise errors.UserAlreadyRegisteredError(ctx.author)

    return commands.check(predicate)


def user_not_in_cooldown():
    def predicate(ctx: discord.ApplicationContext):
        cooldown_end = cooldown_actions.get_cooldown_end_time(ctx.author)
        if cooldown_end is None:
            return True
        else:
            now = int(time.time())
            if not now > cooldown_end:
                seconds_remaining = cooldown_end - now
                raise commands.CommandOnCooldown(commands.Cooldown(1, 900), seconds_remaining, BucketType.user)
            else:
                return True

    return commands.check(predicate)
