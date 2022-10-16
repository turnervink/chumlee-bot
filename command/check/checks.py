from typing import Union

from discord.ext import bridge, commands
from discord.ext.commands import BucketType

from error import errors
from util.database import user_actions, cooldown_actions

import time


def user_registered():
    def predicate(ctx: Union[bridge.BridgeApplicationContext, bridge.BridgeExtContext]):
        author = ctx.message.author if type(ctx) == bridge.BridgeExtContext else ctx.author

        if user_actions.is_registered(author):
            return True
        else:
            raise errors.UserNotRegisteredError(author)
    return commands.check(predicate)


def user_not_registered():
    def predicate(ctx: Union[bridge.BridgeApplicationContext, bridge.BridgeExtContext]):
        author = ctx.message.author if type(ctx) == bridge.BridgeExtContext else ctx.author

        if not user_actions.is_registered(author):
            return True
        else:
            raise errors.UserAlreadyRegisteredError(author)

    return commands.check(predicate)


def user_not_in_cooldown():
    def predicate(ctx: Union[bridge.BridgeApplicationContext, bridge.BridgeExtContext]):
        author = ctx.message.author if type(ctx) == bridge.BridgeExtContext else ctx.author

        cooldown_end = cooldown_actions.get_cooldown_end_time(author)
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


def user_not_in_deal():
    def predicate(ctx: Union[bridge.BridgeApplicationContext, bridge.BridgeExtContext]):
        author = ctx.message.author if type(ctx) == bridge.BridgeExtContext else ctx.author
        guild = ctx.message.guild if type(ctx) == bridge.BridgeExtContext else ctx.guild

        if user_actions.get_is_in_deal(author, guild):
            raise errors.UserAlreadyInDealError(author)
        else:
            return True

    return commands.check(predicate)
