from discord.ext import commands

from util import emoji
from util.database import user_actions, transaction_actions
from util.pawnshop.medal import Medal as MedalObject


class Medal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listmedals", aliases=["medals"], description="See a list of available Chummedals")
    async def list_medals(self, ctx: commands.Context):
        async with ctx.message.channel.typing():
            response = ""

            for medal in MedalObject.VALID_MEDALS:
                response += f"{medal.title()} Chummedal - {MedalObject.MEDAL_DATA[medal]['price']} {emoji.CHUMCOIN}\n"

            await ctx.send(response)

    @commands.command(name="buymedal", description="Buy a Chummedal")
    async def buy_medal(self, ctx: commands.Context, medal_name: str):
        async with ctx.message.channel.typing():
            medal = MedalObject(medal_name.lower())
            user_medals = user_actions.get_medals(ctx.message.author)

            if user_medals is None or medal.name not in user_medals:
                transaction_actions.withdraw(ctx.message.author, medal.price)
                user_actions.award_medal(ctx.message.author, medal)
                response = (f"Awesome! Here's your {medal.name} Chummedal!"
                            "\n\n"
                            f"{ctx.message.author.mention} {emoji.ARROW_RIGHT} {medal.price} "
                            f"{emoji.CHUMCOIN} {emoji.ARROW_RIGHT} {emoji.CHUMLEE}")
                await ctx.send(response)
            else:
                await ctx.send(f"Looks like you've already got the {medal.name} Chummedal {ctx.message.author.mention}!")


def setup(bot: commands.Bot):
    bot.add_cog(Medal(bot))
