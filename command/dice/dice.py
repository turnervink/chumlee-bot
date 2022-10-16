import random

import discord
from discord.ext import commands


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="roll", description="Roll some dice", usage="roll <qty>d<sides>+/-<modifier>")
    async def roll(self, ctx: discord.ApplicationContext, qty: int, sides: int, modifier: int = 0):
        rolls = []
        total = 0
        for i in range(0, qty):
            roll = random.randint(1, sides)
            rolls.append(roll)
            total += roll

        total += modifier
        modifier_prefix = "+" if modifier >= 0 else ""

        embed = discord.Embed(title=f"Roll Result for {qty}d{sides}{modifier_prefix}{modifier}")
        embed.add_field(name="Dice", value=f"({'+'.join(str(x) for x in rolls)}){modifier_prefix}{modifier}", inline=False)
        embed.add_field(name="Result", value=f"{total}", inline=True)
        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Dice(bot))
