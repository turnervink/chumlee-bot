from discord.ext import commands

import logging


logger = logging.getLogger("chumlee-bot")


def handle_command_cooldown_error(ctx, error):
    def time_remaining(seconds: float) -> str:
        if seconds < 60:
            return f"{round(seconds, 0)} seconds"

        minutes = round(seconds / 60)
        return f"{minutes} minutes" if minutes != 1 else f"{minutes} minute"

    if ctx.command.name == "appraise":
        return f"You need to wait {time_remaining(error.retry_after)} " \
               f"until your next appraisal {ctx.message.author.mention}"

    return error


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logger.error(f"Command {ctx.command.name} raised an error for user {ctx.message.author.id}: %s", error)

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(handle_command_cooldown_error(ctx, error))
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f"Usage: {ctx.command.usage}")
        else:
            await ctx.send(error)


def setup(bot: commands.Bot):
    bot.add_cog(CommandErrorHandler(bot))
