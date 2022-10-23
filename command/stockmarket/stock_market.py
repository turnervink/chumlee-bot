import discord
from discord.ext import commands

from util.database import stock_market_actions


class StockMarket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="history")
    async def get_history(
            self,
            ctx: discord.ApplicationContext,
            period: discord.Option(str, choices=["24h", "7d"])
    ):
        await ctx.defer()

        if period == "24h":
            history = stock_market_actions.get_24h_history()
        elif period == "7d":
            history = stock_market_actions.get_7d_history()
        else:
            raise commands.BadArgument("You need to pick either '24h' or '7d' as a history period")

        await ctx.followup.send(str(history))


def setup(bot: commands.Bot):
    bot.add_cog(StockMarket(bot))
