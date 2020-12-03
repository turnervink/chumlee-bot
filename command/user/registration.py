from discord.ext import commands

from command.check import checks
from util.database import user_actions


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='register', description='Register to sell at the pawnshop')
    @checks.user_not_registered()
    async def register(self, ctx):
        async with ctx.message.channel.typing():
            user_actions.register(ctx.message.author)
            await ctx.send(f'You\'re all set {ctx.message.author.mention}!')


def setup(bot: commands.Bot):
    bot.add_cog(Registration(bot))
