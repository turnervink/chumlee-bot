import discord
from discord.ext import commands

from util import emoji
from util.database import user_actions, transaction_actions
from util.pawnshop.medal import Medal as MedalObject


class Medal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="medals", description="See a list of available Chummedals",
                      usage="medals")
    async def list_medals(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        response = ""

        for medal in MedalObject.VALID_MEDALS:
            response += f"{medal.title()} Chummedal - {MedalObject.MEDAL_DATA[medal]['price']} {emoji.CHUMCOIN}\n"

        await ctx.followup.send(response)

    @commands.slash_command(name="buymedal", description="Buy a Chummedal", usage="buymedal <medal name>")
    async def buy_medal(
            self,
            ctx: discord.ApplicationContext,
            medal_name: discord.Option(str, choices=MedalObject.VALID_MEDALS)
    ):
        await ctx.defer()
        medal = MedalObject(medal_name.lower())
        user_medals = user_actions.get_medals(ctx.author)

        if user_medals is None or medal.name not in user_medals:
            transaction_actions.withdraw(ctx.author, medal.price)
            user_actions.award_medal(ctx.author, medal)
            response = (f"Awesome! Here's your {medal.name} Chummedal!"
                        "\n\n"
                        f"{ctx.author.mention} {emoji.ARROW_RIGHT} {medal.price} "
                        f"{emoji.CHUMCOIN} {emoji.ARROW_RIGHT} {emoji.CHUMLEE}")
            await ctx.followup.send(response)
        else:
            await ctx.followup.send(f"Looks like you've already got the {medal.name} Chummedal {ctx.author.mention}!")


def setup(bot: commands.Bot):
    bot.add_cog(Medal(bot))
