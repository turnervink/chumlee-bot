import discord
from discord.ext import bridge, commands

from command.check import checks
from error import errors
from util import emoji
from util.database import transaction_actions, user_actions


class UserTransaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="pay", description="Pay another user some Chumcoins", usage="pay <@user> <amount>")
    @checks.user_registered()
    async def pay(self, ctx: bridge.BridgeApplicationContext, payee: discord.User, amount: int):
        async with ctx.typing():
            payer = ctx.author

            if payer == payee:
                raise errors.TransactionUsersAreEqualError(payer)

            if payee == self.bot.user:
                raise commands.BadArgument(f"I appreciate it, {payer.mention}, but I can't take your {emoji.CHUMCOIN}s!")

            if not user_actions.is_registered(payee):
                raise errors.UserNotFoundError(payee)

            if amount <= 0:
                raise commands.BadArgument("You can't pay someone a value that's zero or less!")

            transaction_actions.withdraw(payer, amount)
            transaction_actions.deposit(payee, amount)

            await ctx.respond(f"{ctx.author.mention} {emoji.ARROW_RIGHT} {amount} {emoji.CHUMCOIN} "
                           f"{emoji.ARROW_RIGHT} {payee.mention}")


def setup(bot: commands.Bot):
    bot.add_cog(UserTransaction(bot))
