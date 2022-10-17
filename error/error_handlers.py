import logging

import discord
from discord.ext import commands

from error.errors import BotError

logger = logging.getLogger("chumlee-bot")


def handle_command_cooldown_error(ctx: discord.ApplicationContext, error):
    def time_remaining(seconds: float) -> str:
        if seconds < 60:
            return f"{round(seconds, 0)} seconds"

        minutes = round(seconds / 60)
        return f"{minutes} minutes" if minutes != 1 else f"{minutes} minute"

    if ctx.command.name == "appraise":
        return f"You need to wait {time_remaining(error.retry_after)} " \
               f"until your next appraisal {ctx.author.mention}"

    return error


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if ctx.command is not None:
            logger.error(f"Command {ctx.command.name} raised an error for user {ctx.author.id}: %s", error)
        else:
            logger.error(f"Command was None in error for user {ctx.author.id}: %s", error)

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(handle_command_cooldown_error(ctx, error))
        elif isinstance(error, BotError):
            await ctx.respond(error)
        else:
            await ctx.respond("Whoops! Something went wrong.")


def setup(bot: commands.Bot):
    bot.add_cog(CommandErrorHandler(bot))
