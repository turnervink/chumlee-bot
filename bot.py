import json
import os

import discord

from error.errors import InvalidChannelError
from util import log
from util.database import guild_actions

logger = log.setup_logger("chumlee-bot")

try:
    debug_guild_ids = json.loads(os.environ['DEBUG_GUILD_IDS'])
    logger.info("Starting bot with debug_guilds=" + str(debug_guild_ids))
    bot = discord.Bot(debug_guilds=debug_guild_ids)
except KeyError:
    logger.info("No debug_guilds specified, will create global commands")
    bot = discord.Bot()


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
async def is_not_dm(ctx: discord.ApplicationContext):
    return not isinstance(ctx.channel, discord.DMChannel)


@bot.event
async def on_ready():
    logger.info(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

    guilds = list(guild.name for guild in bot.guilds)
    logger.info(f"Logged in on: {guilds}")


bot.load_extension("util.status")
bot.load_extension("util.channel_bind")
bot.load_extension("util.stockmarket.stock_market")
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
