from typing import Union

import discord
from discord.ext import commands

from error.errors import InvalidChannelError
from util import log, message_triggers
from util.database import guild_actions

import os
import random

ALLOWED_CHANNELS = ["bot-testing", "the-pawnshop"]  # Names of channels where bot commands can be used

intents = discord.Intents(messages=True, reactions=True, message_content=True, guilds=True)
bot = commands.Bot(command_prefix=".", intents=intents)


# Until everything is a slash command we need to check the context type to infer
# if it is, since slash commands won't have `message` on the context
@bot.check
async def is_in_allowed_channel(ctx: Union[commands.Context, discord.ApplicationContext]):
    if ctx.command.name in ["allowchannel", "disallowchannel", "allowedchannels", "roll"]:
        return True

    allowed_channels = guild_actions.get_allowed_channels(str(ctx.guild.id))
    if allowed_channels is not None and str(ctx.channel.id) in list(allowed_channels.keys()):
        return True
    else:
        if type(ctx) is commands.Context:
            raise InvalidChannelError(ctx.message.author)
        else:
            raise InvalidChannelError(ctx.author)


@bot.check
async def is_not_dm(ctx: Union[commands.Context, discord.ApplicationContext]):
    if type(ctx) is commands.Context:
        return not isinstance(ctx.message.channel, discord.DMChannel)
    else:
        return not isinstance(ctx.channel, discord.DMChannel)


@bot.event
async def on_message(message: discord.Message):
    if message.author != bot.user:
        if any(trigger in message.content.lower() for trigger in message_triggers.REACTION_TRIGGERS):
            chumlee_emoji = discord.utils.get(bot.emojis, name="chumlee")
            if chumlee_emoji is not None:
                await message.add_reaction(chumlee_emoji)
        elif any (trigger in message.content.lower() for trigger in message_triggers.YOUTUBE_LINK_TRIGGERS):
            quote = random.choice(message_triggers.YOUTUBE_VIDEO_QUOTES)
            await message.channel.send(f"{quote}\n\n{message_triggers.YOUTUBE_LINK}")
        else:
            await bot.process_commands(message)


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
