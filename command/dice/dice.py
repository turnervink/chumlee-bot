from discord.ext import commands
from discord.ext.commands import CommandError

import random


def split_roll(roll: str):
    split = str.lower(roll).split('d')
    print(split)
    if len(split) != 2:
        raise CommandError("Usage: .roll 1d20 +1")

    try:
        if split[0] == "":
            split[0] = "1"

        qty = int(split[0])
        sides = int(split[1])
    except ValueError:
        raise CommandError("Usage: .roll 1d20 +1")

    return qty, sides


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll")
    async def roll(self, ctx: commands.Context, roll: str, modifier: int = 0):
        qty, sides = split_roll(roll)

        rolls = []
        total = 0
        for i in range(0, qty):
            roll = random.randint(1, sides)
            rolls.append(roll)
            total += roll

        total += modifier
        modifier_prefix = "+" if modifier >= 0 else ""

        await ctx.send(
            f"{ctx.message.author.mention}: "
            f"`{qty}d{sides}` = ({'+'.join(str(x) for x in rolls)}){modifier_prefix}{modifier} = {total}"
        )


def setup(bot: commands.Bot):
    bot.add_cog(Dice(bot))
