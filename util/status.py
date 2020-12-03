import discord
from discord.ext import commands, tasks

import random


STATUSES = [
    "Collecting shoes",
    "Enjoying some Western Alalia",
    "Preparing the circle of beauty",
    "In the Chum Chum Room"
]


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status.start()

    @tasks.loop(hours=2)
    async def update_status(self):
        await self.bot.change_presence(activity=discord.Game(name=random.choice(STATUSES)))

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
