import random
from asyncio import sleep

import discord
from discord.ext import commands

from command.check import checks
from error.errors import LottoInProgressError, InsufficientFundsError
from util import emoji
from util.database import transaction_actions, user_actions
from util.pawnshop.lottodetails import LottoDetails
from view.pawnshop.LottoStartView import LottoStartView

BETTING_WINDOW_LENGTH_SECONDS = 60


class Lotto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lotteries_in_progress = []

    @commands.slash_command(name="lotto", description="Start a Chumlottery", usage="lotto <bet amount>")
    @checks.user_registered()
    async def start_lotto(self, ctx: discord.ApplicationContext, bet: int):
        await ctx.defer()

        if bet <= 0:
            raise commands.BadArgument("You can't bet a value that's zero or less!")

        if ctx.guild.id in self.lotteries_in_progress:
            raise LottoInProgressError

        if user_actions.get_balance(ctx.author) < bet:
            raise InsufficientFundsError(ctx.author)

        lotto = LottoDetails(
            bet,
            BETTING_WINDOW_LENGTH_SECONDS,
            ctx.guild,
            ctx.author,
            ctx.channel,
            [ctx.author]
        )
        self.lotteries_in_progress.append(ctx.guild.id)

        await ctx.followup.send(
            lotto.message(),
            view=LottoStartView(
                lotto=lotto,
                betting_window_sec=BETTING_WINDOW_LENGTH_SECONDS,
                run_lotto_callback=self.run_lotto
            )
        )

    async def run_lotto(self, lotto: LottoDetails):
        if not len(lotto.players) > 1:
            await lotto.channel.send("No one else joined the Chumlottery, so it cannot run.")
        else:
            await lotto.channel.send("Alright! No more bets!"
                           "\n"
                           f"Collecting {lotto.bet} {emoji.CHUMCOIN} from all the players...")

            prize = 0
            for player in lotto.players:
                transaction_actions.withdraw(player, lotto.bet)
                prize += lotto.bet

            await sleep(1)
            await lotto.channel.send(f"Rolling... {emoji.GAME_DIE}")
            winner = random.choice(lotto.players)
            await sleep(random.randint(1, 5))

            await lotto.channel.send(f"Congratulations {winner.mention}! You won {prize} {emoji.CHUMCOIN}!"
                           "\n\n"
                           f"{emoji.CHUMLEE} {emoji.ARROW_RIGHT} {prize} {emoji.CHUMCOIN} "
                           f"{emoji.ARROW_RIGHT} {winner.mention}")
            transaction_actions.deposit(winner, prize)

        self.lotteries_in_progress.remove(lotto.guild.id)


def setup(bot: commands.Bot):
    bot.add_cog(Lotto(bot))
