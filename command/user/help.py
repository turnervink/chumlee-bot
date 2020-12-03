from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="Show help info")
    async def help(self, ctx):
        async with ctx.message.channel.typing():
            welcome_message = ("Hi! I'm Chumlee, and I run this pawn shop. To get started, "
                               f"use **{self.bot.command_prefix}register**, then "
                               f"use **{self.bot.command_prefix}commands** to see what I can do!")

            await ctx.send(welcome_message)

    @commands.command(name="commands", description="List all commands")
    async def commands(self, ctx):
        async with ctx.message.channel.typing():
            response = "```"
            for command in self.bot.commands:
                response += f"{command.name} - {command.description}\n"
            response += "```"

            await ctx.send(response)


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))