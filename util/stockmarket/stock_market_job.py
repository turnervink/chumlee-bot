import logging
import os
from datetime import time, timezone

from discord.ext import commands, tasks

from util.database import stock_market_actions
from util.stockmarket import stock_price

logger = logging.getLogger("chumlee-bot")

# Update each hour on the hour, except in dev where it is more frequent for easier testing
if os.environ["DB_ROOT"] == "development":
    logger.info("Running in dev, so updating the stock price every minute")
    STOCK_PRICE_UPDATE_TIMES = {"minutes": 1}
else:
    STOCK_PRICE_UPDATE_TIMES = {"time": [time(hour=h, tzinfo=timezone.utc) for h in range(24)]}


class StockMarketJob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_stock_price.start()

    @tasks.loop(**STOCK_PRICE_UPDATE_TIMES)
    async def update_stock_price(self):
        logger.debug("Updating stock price...")

        current_price = stock_market_actions.get_current_price()
        logger.debug("Current price is: " + str(current_price))

        updated_price = stock_price.get_new_price(current_price)
        logger.debug("New price is: " + str(updated_price))

        stock_market_actions.set_current_price(updated_price)
        stock_market_actions.append_to_history(updated_price)

    @update_stock_price.before_loop
    async def before_update_stock_price(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(StockMarketJob(bot))
