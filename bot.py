from discord.ext import commands

from command.error.errors import InvalidChannelError
from util import log

import os

ALLOWED_CHANNELS = ["bot-testing", "the-pawnshop"]  # Names of channels where bot commands can be used

bot = commands.Bot(command_prefix=".")


@bot.check
async def is_in_valid_channel(ctx: commands.Context):
    if ctx.command.name == "help" or ctx.channel.name in ALLOWED_CHANNELS:
        return True
    else:
        raise InvalidChannelError(ctx.message.author)


@bot.event
async def on_ready():
    bot.load_extension("command.error.error_handlers")
    bot.load_extension("command.user.help")
    bot.load_extension("command.user.registration")
    bot.load_extension("command.user.profile")
    bot.load_extension("command.user.transaction")
    bot.load_extension("command.pawnshop.transaction")
    bot.load_extension("command.pawnshop.medal")
    bot.load_extension("command.pawnshop.lotto")
    bot.load_extension("util.status")

    logger = log.setup_logger("chumlee-bot")
    logger.info(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

bot.run(os.environ['BOT_TOKEN'])
