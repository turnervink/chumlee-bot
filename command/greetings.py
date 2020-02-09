import discord
from discord.ext import commands

from command.user.help import Help


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', aliases=['hi', 'yo'])
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send('Hello {0.name}'.format(member))


def setup(bot: commands.Bot):
    bot.add_cog(Greetings(bot))
