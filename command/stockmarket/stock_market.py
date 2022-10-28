import logging
from datetime import datetime

import discord
from dateutil import tz
from discord.ext import commands

from error.errors import InsufficientFundsError, InsufficientStockError
from util import emoji
from util.database import stock_market_actions, user_actions, transaction_actions
from util.stockmarket import stock_price


class StockMarket(commands.Cog):
    stock_commands = discord.SlashCommandGroup("stocks", "Stock market commands")

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("chumlee-bot")

    @stock_commands.command(name="buy", description="Buy $CHUM")
    async def buy_stock(self, ctx: discord.ApplicationContext, qty: int):
        await ctx.defer()

        current_stock_price = stock_market_actions.get_current_price()
        purchase_price_total = current_stock_price * qty

        if user_actions.get_balance(ctx.author) < purchase_price_total:
            raise InsufficientFundsError(ctx.author)

        transaction_actions.withdraw(ctx.author, purchase_price_total)
        stock_market_actions.buy_stock(ctx.author, qty, current_stock_price)

        await ctx.followup.send(f"Purchased {qty} **$CHUM** at {current_stock_price} {emoji.CHUMCOIN}/share\n"
                                f"Total purchase price: {purchase_price_total} {emoji.CHUMCOIN}")

    @stock_commands.command(name="sell", description="Sell $CHUM")
    async def sell_stock(self, ctx: discord.ApplicationContext, qty: int):
        await ctx.defer()

        current_user_portfolio = stock_market_actions.get_user_portfolio(ctx.author)
        if current_user_portfolio["stockQty"] < qty:
            raise InsufficientStockError(ctx.author)

        current_stock_price = stock_market_actions.get_current_price()
        sale_price_total = current_stock_price * qty

        stock_market_actions.sell_stock(ctx.author, qty, current_stock_price)
        transaction_actions.deposit(ctx.author, sale_price_total)

        await ctx.followup.send(f"Sold {qty} **$CHUM** at {current_stock_price} {emoji.CHUMCOIN}/share\n"
                                f"Total sale price: {sale_price_total} {emoji.CHUMCOIN}")

    @stock_commands.command(name="price", description="Check the price of $CHUM")
    async def get_price(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        current_price = int(stock_market_actions.get_current_price())
        await ctx.followup.send(f"**$CHUM** is trading at {current_price} {emoji.CHUMCOIN}/share")

    @stock_commands.command(name="pricehistory", description="Get the price history of $CHUM")
    async def get_history(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        history = stock_market_actions.get_24h_history()
        current_price = stock_market_actions.get_current_price()
        change_pct = stock_price.calculate_price_change_pct(history[0], history[-1])

        price_graph = stock_price.graph_price_history(history)

        if change_pct > 0:
            arrow_image = discord.File("resources/up.png", filename="changeicon.png")
        elif change_pct < 0:
            arrow_image = discord.File("resources/down.png", filename="changeicon.png")
        else:
            arrow_image = discord.File("resources/flat.png", filename="changeicon.png")

        embed = discord.Embed(title="**$CHUM**", description="Last 24 hours")
        embed.set_image(url="attachment://plot.png")
        embed.set_thumbnail(url="attachment://changeicon.png")
        embed.add_field(name="Current Price", value=f"{current_price} {emoji.CHUMCOIN}/share", inline=True)
        embed.add_field(name="Change", value=f"{change_pct}%", inline=True)
        embed.add_field(name="Low", value=f"{int(min(history))} {emoji.CHUMCOIN}/share", inline=False)
        embed.add_field(name="High", value=f"{int(max(history))} {emoji.CHUMCOIN}/share", inline=True)

        await ctx.followup.send(embed=embed, files=[price_graph, arrow_image])

    @stock_commands.command(name="portfolio", description="Check how much $CHUM you own")
    async def get_portfolio(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        portfolio = stock_market_actions.get_user_portfolio(ctx.author)
        current_stock_price = stock_market_actions.get_current_price()

        portfolio_value = portfolio['stockQty'] * current_stock_price

        embed = discord.Embed(title="Your Portfolio")
        embed.add_field(name="Current Holdings",
                        value=f"{portfolio['stockQty']} **$CHUM** at {current_stock_price} {emoji.CHUMCOIN}/share",
                        inline=True)
        embed.add_field(name="Total Value", value=f"{str(portfolio_value)} {emoji.CHUMCOIN}", inline=True)

        try:
            history = stock_market_actions.get_user_portfolio(ctx.author)["history"]
            history.sort(key=lambda t: t["timestamp"], reverse=True)

            history_response = ""
            for trade in history[:10]:
                trade_time = datetime.strptime(trade["timestamp"], "%Y-%m-%d %H:%M:%S.%f%z")
                trade_time.replace(tzinfo=tz.gettz("utc"))
                trade_time = trade_time.astimezone(tz.gettz("Canada/Pacific"))

                history_response += f"_{trade_time.strftime('%d %b %Y %H:%M %Z')}_ - " \
                                    f"{trade['action'].upper()} {trade['qty']} **$CHUM** at " \
                                    f"{trade['price']} {emoji.CHUMCOIN}/share\n"

            embed.add_field(name="Last 10 Trades", value=history_response, inline=False)
        except KeyError:
            self.logger.warning("No history found for user %s", ctx.author)

        await ctx.followup.send(embed=embed)

    @stock_commands.command(name="tradehistory", description="See trade history for your portfolio")
    async def get_portfolio_history(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        history = stock_market_actions.get_user_portfolio(ctx.author)["history"]
        response = "Your trade history:\n"
        for trade in history:
            trade_time = datetime.strptime(trade["timestamp"], "%Y-%m-%d %H:%M:%S.%f%z")
            trade_time.replace(tzinfo=tz.gettz("utc"))
            trade_time = trade_time.astimezone(tz.gettz("Canada/Pacific"))

            response += f"{trade_time.strftime('%d %b %Y %H:%M %Z')} - " \
                        f"{trade['action'].upper()} {trade['qty']} **$CHUM** at " \
                        f"{trade['price']} {emoji.CHUMCOIN}/share\n"

        await ctx.user.send(response)
        await ctx.followup.send("Sent your full trade history in a DM")


def setup(bot: commands.Bot):
    bot.add_cog(StockMarket(bot))
