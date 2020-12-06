from asyncio import sleep
from discord.ext import commands

from command.check import checks
from command.error.errors import LottoInProgressError, NoLottoInProgressError, UserAlreadyInLottoError
from util.database.error.errors import InsufficientFundsError
from util import emoji
from util.database import transaction_actions, user_actions

import random


BETTING_WINDOW_LENGTH_SECONDS = 60


class Lotto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lotteries = {}

    @commands.command(name="lotto", aliases=["lottery", "chumlotto", "chumlottery"], description="Start a Chumlottery",
                      usage="lotto <bet amount>")
    @checks.user_registered()
    async def start_lotto(self, ctx: commands.Context, bet: int):
        if bet <= 0:
            raise commands.BadArgument("You can't bet a value that's zero or less!")

        if ctx.guild.id in self.lotteries:
            raise LottoInProgressError

        if user_actions.get_balance(ctx.message.author) < bet:
            raise InsufficientFundsError(ctx.message.author)

        self.lotteries[ctx.guild.id] = {
            "bet": bet,
            "players": [
                ctx.message.author
            ]
        }

        egg = " Nice." if bet == 69 else ""
        async with ctx.message.channel.typing():
            await ctx.send(f"{ctx.message.author.mention} has started a Chumlottery!{egg}"
                           "\n\n"
                           f"Type **{self.bot.command_prefix}bet** to bet {bet} {emoji.CHUMCOIN} and join! Bets are open "
                           f"for {BETTING_WINDOW_LENGTH_SECONDS} seconds.")

        await sleep(BETTING_WINDOW_LENGTH_SECONDS)

        async with ctx.message.channel.typing():
            if not len(self.lotteries[ctx.guild.id]["players"]) > 1:
                await ctx.send("No one else joined the Chumlottery, so it cannot run.")
            else:
                await ctx.send("Alright! No more bets!"
                               "\n"
                               f"Collecting {bet} {emoji.CHUMCOIN} from all the players...")

                prize = 0
                for player in self.lotteries[ctx.guild.id]["players"]:
                    transaction_actions.withdraw(player, bet)
                    prize += bet

                await sleep(1)
                await ctx.send(f"Rolling... {emoji.GAME_DIE}")
                winner = random.choice(self.lotteries[ctx.guild.id]["players"])
                await sleep(random.randint(1, 5))

                await ctx.send(f"Congratulations {winner.mention}! You won {prize} {emoji.CHUMCOIN}!"
                               "\n\n"
                               f"{emoji.CHUMLEE} {emoji.ARROW_RIGHT} {prize} {emoji.CHUMCOIN} "
                               f"{emoji.ARROW_RIGHT} {winner.mention}")
                transaction_actions.deposit(winner, prize)

            self.lotteries.pop(ctx.guild.id)

    @commands.command(name="bet", description="Join a Chumlottery", hidden=True)
    async def join_lotto(self, ctx: commands.Context):
        async with ctx.message.channel.typing():
            if ctx.guild.id not in self.lotteries:
                raise NoLottoInProgressError

            if any(player.id == ctx.message.author.id for player in self.lotteries[ctx.guild.id]["players"]):
                raise UserAlreadyInLottoError(ctx.message.author)

            if user_actions.get_balance(ctx.message.author) < self.lotteries[ctx.guild.id]["bet"]:
                raise InsufficientFundsError(ctx.message.author)

            self.lotteries[ctx.guild.id]["players"].append(ctx.message.author)
            await ctx.message.add_reaction("✅")


def setup(bot: commands.Bot):
    bot.add_cog(Lotto(bot))
