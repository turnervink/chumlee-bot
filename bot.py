import discord
from discord.ext import commands

from command.error.errors import InvalidChannelError
from util import log
from util.database import guild_actions

import os

ALLOWED_CHANNELS = ["bot-testing", "the-pawnshop"]  # Names of channels where bot commands can be used

bot = commands.Bot(command_prefix=".")


@bot.check
async def is_in_allowed_channel(ctx: commands.Context):
    if ctx.command.name in ["allowchannel", "disallowchannel", "allowedchannels"]:
        return True

    allowed_channels = list(guild_actions.get_allowed_channels(ctx.guild.id).keys())
    if str(ctx.channel.id) in allowed_channels:
        return True
    else:
        raise InvalidChannelError(ctx.message.author)


@bot.check
async def is_not_dm(ctx: commands.Context):
    return not isinstance(ctx.message.channel, discord.DMChannel)


@bot.event
async def on_ready():
    bot.load_extension("util.status")
    bot.load_extension("util.channel_bind")
    bot.load_extension("command.error.error_handlers")
    bot.load_extension("command.user.help")
    bot.load_extension("command.user.registration")
    bot.load_extension("command.user.profile")
    bot.load_extension("command.user.transaction")
    bot.load_extension("command.pawnshop.transaction")
    bot.load_extension("command.pawnshop.medal")
    bot.load_extension("command.pawnshop.lotto")

    logger = log.setup_logger("chumlee-bot")
    logger.info(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

bot.run(os.environ['BOT_TOKEN'])
