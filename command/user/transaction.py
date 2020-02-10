import discord
from discord.ext import commands

from command.check import checks
from util.database import transaction_actions


class Transaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pay', description='Pay another user some Chumcoins')
    @checks.user_registered()
    async def pay(self, ctx, payee: discord.User, amount: int):
        payer = ctx.message.author
        result = transaction_actions.transfer(payer, payee, amount)
        await ctx.send(result)


def setup(bot: commands.Bot):
    bot.add_cog(Transaction(bot))
