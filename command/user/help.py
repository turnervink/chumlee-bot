from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', description='Show help info')
    async def help(self, ctx, *cog):
        welcome_message = ("Hi! I'm Chumlee, and I run this pawn shop. To get started, "
                           "use **.register**, then use **.commands** to see what I can do!")

        await ctx.send(welcome_message)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))