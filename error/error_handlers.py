from typing import Union

import discord
from discord.ext import commands, bridge

import logging

from error.errors import NoItemToAppraiseError

logger = logging.getLogger("chumlee-bot")


def handle_command_cooldown_error(ctx: Union[bridge.BridgeApplicationContext, bridge.BridgeExtContext], error):
    author = ctx.message.author if type(ctx) == bridge.BridgeExtContext else ctx.author

    def time_remaining(seconds: float) -> str:
        if seconds < 60:
            return f"{round(seconds, 0)} seconds"

        minutes = round(seconds / 60)
        return f"{minutes} minutes" if minutes != 1 else f"{minutes} minute"

    if ctx.command.name == "appraise":
        return f"You need to wait {time_remaining(error.retry_after)} " \
               f"until your next appraisal {author.mention}"

    return error


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: bridge.BridgeExtContext, error):
        if ctx.command is not None:
            logger.error(f"Command {ctx.command.name} raised an error for user {ctx.message.author.id}: %s", error)
        else:
            logger.error(f"Command was None in error for user {ctx.message.author.id}: %s", error)

        if hasattr(ctx.command, "on_error"):
            return

        if ctx.command is None and ctx.message.content[1] == '.':
            return

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(handle_command_cooldown_error(ctx, error))
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f"Usage: {ctx.command.usage}")
        else:
            return await ctx.send(error)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: bridge.BridgeApplicationContext, error: discord.DiscordException):
        if ctx.command is not None:
            logger.error(f"Command {ctx.command.name} raised an error for user {ctx.author.id}: %s", error)
        else:
            logger.error(f"Command was None in error for user {ctx.author.id}: %s", error)

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.respond(handle_command_cooldown_error(ctx, error))
        elif isinstance(error, NoItemToAppraiseError):
            return await ctx.respond("You must include some text or an image to appraise")
        else:
            return await ctx.respond(f"Sorry, that didn't work! Please check the command usage and try again.")


def setup(bot: commands.Bot):
    bot.add_cog(CommandErrorHandler(bot))
