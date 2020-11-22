import discord
from discord.ext import commands

from command.check import checks
from util.database import transaction_actions, user_actions
from command.error import errors


class Transaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pay', description='Pay another user some Chumcoins', usage="pay <mention a user> <an "
                                                                                       "amount as a positive number>")
    @checks.user_registered()
    async def pay(self, ctx, payee: discord.User, amount: int):
        payer = ctx.message.author
        
        if payer == payee:
            raise errors.TransactionUsersAreEqualError(payer)

        if not user_actions.is_registered(payee):
            raise errors.UserNotRegisteredError(payee)

        if amount <= 0:
            raise commands.BadArgument("You can't pay someone a value that's zero or less!")

        transaction_actions.withdraw(payer, amount)
        transaction_actions.deposit(payee, amount)


def setup(bot: commands.Bot):
    bot.add_cog(Transaction(bot))
