import discord
from discord.ext import commands

from command.check import checks
from util.database import transaction_actions, user_actions
from util import emoji
from error import errors


class UserTransaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pay", description="Pay another user some Chumcoins", usage="pay <@user> <amount>")
    @checks.user_registered()
    async def pay(self, ctx, payee: discord.User, amount: int):
        async with ctx.typing():
            payer = ctx.message.author

            if payer == payee:
                raise errors.TransactionUsersAreEqualError(payer)

            if not user_actions.is_registered(payee):
                raise errors.UserNotRegisteredError(payee)

            if amount <= 0:
                raise commands.BadArgument("You can't pay someone a value that's zero or less!")

            transaction_actions.withdraw(payer, amount)
            transaction_actions.deposit(payee, amount)

            await ctx.send(f"{ctx.message.author.mention} {emoji.ARROW_RIGHT} {amount} {emoji.CHUMCOIN} "
                           f"{emoji.ARROW_RIGHT} {payee.mention}")


def setup(bot: commands.Bot):
    bot.add_cog(UserTransaction(bot))
