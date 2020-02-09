from discord.ext import commands

from command.check import checks
from util.database import user_actions
from util.emoji import CHUMCOIN


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='profile', description='View your profile')
    @checks.user_registered()
    async def profile(self, ctx):
        await ctx.send('Here\'s your profile!')

    @commands.command(name='balance', aliases=['bal'], description='Get your Chumcoin balance')
    @checks.user_registered()
    async def balance(self, ctx):
        balance = user_actions.get_balance(ctx.message.author)
        await ctx.send(f'{ctx.message.author.mention} your balance is {balance} {CHUMCOIN}')


def setup(bot: commands.Bot):
    bot.add_cog(Profile(bot))
