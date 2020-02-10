from discord.ext import commands

from command.error import errors
from util.database import user_actions


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


def user_not_in_deal():
    def predicate(ctx):
        if not user_actions.is_in_deal(ctx.message.author):
            return True
        else:
            raise errors.UserAlreadyInDealError(ctx.message.author)

    return commands.check(predicate)


def message_has_item_to_appraise():
    def predicate(ctx):
        if len(str.split(ctx.message.content)) > 1 or len(ctx.message.attachments) != 0:
            return True
        else:
            raise errors.NoItemToAppraiseError(ctx.message.author)

    return commands.check(predicate)
