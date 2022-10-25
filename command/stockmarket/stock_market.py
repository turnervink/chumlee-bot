import discord
from discord.ext import commands

from error.errors import InsufficientFundsError, InsufficientStockError
from util import emoji
from util.database import stock_market_actions, user_actions, transaction_actions
from util.stockmarket import stock_price


class StockMarket(commands.Cog):
    stock_commands = discord.SlashCommandGroup("stocks", "Stock market commands")

    def __init__(self, bot):
        self.bot = bot

    @stock_commands.command(name="buy", description="Buy $CHUM")
    async def buy_stock(self, ctx: discord.ApplicationContext, qty: int):
        await ctx.defer()

        current_stock_price = stock_market_actions.get_current_price()
        purchase_price_total = current_stock_price * qty

        if user_actions.get_balance(ctx.author) < purchase_price_total:
            raise InsufficientFundsError(ctx.author)

        transaction_actions.withdraw(ctx.author, purchase_price_total)
        stock_market_actions.buy_stock(ctx.author, qty)

        await ctx.followup.send(f"Purchased {qty} **$CHUM** at {current_stock_price} {emoji.CHUMCOIN}\n"
                                f"Total purchase price: {purchase_price_total} {emoji.CHUMCOIN}")

    @stock_commands.command(name="sell", description="Sell $CHUM")
    async def sell_stock(self, ctx: discord.ApplicationContext, qty: int):
        await ctx.defer()

        current_user_portfolio = stock_market_actions.get_user_portfolio(ctx.author)
        if current_user_portfolio["stockQty"] < qty:
            raise InsufficientStockError(ctx.author)

        current_stock_price = stock_market_actions.get_current_price()
        sale_price_total = current_stock_price * qty

        stock_market_actions.sell_stock(ctx.author, qty)
        transaction_actions.deposit(ctx.author, sale_price_total)

        await ctx.followup.send(f"Sold {qty} **$CHUM** at {current_stock_price} {emoji.CHUMCOIN}\n"
                                f"Total sale price: {sale_price_total} {emoji.CHUMCOIN}")

    @stock_commands.command(name="price", description="Check the price of $CHUM")
    async def get_price(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        current_price = int(stock_market_actions.get_current_price())
        await ctx.followup.send(f"**$CHUM** is trading at {current_price} {emoji.CHUMCOIN}")

    @stock_commands.command(name="pricehistory", description="Get the price history of $CHUM")
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

        price_graph = stock_price.graph_price_history(history)

        await ctx.followup.send(file=price_graph)

    @stock_commands.command(name="portfolio", description="Check how much $CHUM you own")
    async def get_portfolio(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        portfolio = stock_market_actions.get_user_portfolio(ctx.author)
        current_stock_price = stock_market_actions.get_current_price()
        await ctx.followup.send(
            f"You currently own {portfolio['stockQty']} **$CHUM** at {current_stock_price} {emoji.CHUMCOIN}\n"
            f"Total portfolio value: {portfolio['stockQty'] * current_stock_price} {emoji.CHUMCOIN}"
        )


def setup(bot: commands.Bot):
    bot.add_cog(StockMarket(bot))
