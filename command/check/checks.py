from discord.ext import commands

from command.error import errors
from util.database import user_actions, cooldown_actions

import time


def user_registered():
    def predicate(ctx):
        if user_actions.is_registered(ctx.message.author):
            return True
        else:
            raise errors.UserNotRegisteredError(ctx.message.author)
    return commands.check(predicate)


def user_not_registered():
    def predicate(ctx):
        if not user_actions.is_registered(ctx.message.author):
            return True
        else:
            raise errors.UserAlreadyRegisteredError(ctx.message.author)

    return commands.check(predicate)


def user_not_in_cooldown():
    def predicate(ctx):
        cooldown_end = cooldown_actions.get_cooldown_end_time(ctx.message.author)
        if cooldown_end is None:
            return True
        else:
            now = int(time.time())
            if not now > cooldown_end:
                seconds_remaining = cooldown_end - now
                raise commands.CommandOnCooldown(commands.cooldown(1, 900), seconds_remaining)
            else:
                return True

    return commands.check(predicate)


def message_has_item_to_appraise():
    def predicate(ctx):
        if len(str.split(ctx.message.content)) > 1 or len(ctx.message.attachments) != 0:
            return True
        else:
            raise errors.NoItemToAppraiseError(ctx.message.author)

    return commands.check(predicate)
