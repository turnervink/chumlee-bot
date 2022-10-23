import logging
import os
from datetime import time, timezone

from discord.ext import commands, tasks

logger = logging.getLogger("chumlee-bot")

# Update each hour on the hour, except in dev where its every minute for easier testing
if os.environ["DB_ROOT"] == "development":
    logger.info("Running in dev, so updating the stock price every minute")
    STOCK_PRICE_UPDATE_TIMES = [time(minute=m, tzinfo=timezone.utc) for m in range(60)]
else:
    STOCK_PRICE_UPDATE_TIMES = [time(hour=h, tzinfo=timezone.utc) for h in range(24)]


class StockMarket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_stock_price.start()

    @tasks.loop(time=STOCK_PRICE_UPDATE_TIMES)
    async def update_stock_price(self):
        logger.debug("Updating stock price...")

    @update_stock_price.before_loop
    async def before_update_stock_price(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(StockMarket(bot))
