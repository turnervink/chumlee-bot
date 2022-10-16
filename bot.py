from typing import Union

import discord
from discord.ext import bridge, commands

from error.errors import InvalidChannelError
from util import log, message_triggers
from util.database import guild_actions

import os
import random

ALLOWED_CHANNELS = ["bot-testing", "the-pawnshop"]  # Names of channels where bot commands can be used

intents = discord.Intents(messages=True, reactions=True, message_content=True, guilds=True)
bot = discord.Bot(intents=intents, debug_guilds=[339533012725268480])


@bot.check
async def is_in_allowed_channel(ctx: discord.ApplicationContext):
    if ctx.command.name in ["allowchannel", "disallowchannel", "allowedchannels", "roll"]:
        return True

    allowed_channels = guild_actions.get_allowed_channels(str(ctx.guild.id))
    if allowed_channels is not None and str(ctx.channel.id) in list(allowed_channels.keys()):
        return True
    else:
        raise InvalidChannelError(ctx.author)


@bot.check
async def is_not_dm(ctx):
    print(type(ctx))
    if type(ctx) is commands.Context:
        return not isinstance(ctx.message.channel, discord.DMChannel)
    else:
        return not isinstance(ctx.channel, discord.DMChannel)


@bot.event
async def on_ready():
    logger = log.setup_logger("chumlee-bot")
    logger.info(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

    guilds = list(guild.name for guild in bot.guilds)
    logger.info(f"Logged in on: {guilds}")


bot.load_extension("util.status")
bot.load_extension("util.channel_bind")
bot.load_extension("error.error_handlers")
bot.load_extension("command.user.help")
bot.load_extension("command.user.registration")
bot.load_extension("command.user.profile")
bot.load_extension("command.user.usertransaction")
bot.load_extension("command.pawnshop.pawnshoptransaction")
bot.load_extension("command.pawnshop.medal")
bot.load_extension("command.pawnshop.lotto")
bot.load_extension("command.dice.dice")
bot.run(os.environ['BOT_TOKEN'])
