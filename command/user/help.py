import discord
from discord.ext import commands

from util.emoji import CHUMCOIN


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        welcome_embed = discord.Embed(title="Hi! I'm Chumlee, and I run this pawnshop.",
                                      colour=discord.Colour(0xffffff),
                                      description="I'm here to appraise your memes, jokes, and anything else you can "
                                                  f"think of. I'll offer you Chumcoins {CHUMCOIN} in exhange, and the "
                                                  "more you collect the more you'll level up. You can trade in your "
                                                  f"Chumcoins {CHUMCOIN} for different Chummedals to display on your ."
                                                  "profile")
        welcome_embed.add_field(name="Register a channel",
                                value=f"Use **/allowchannel** so I can interact with people there",
                                inline=False)
        welcome_embed.add_field(name="Get an appraisal",
                                value=f"Use **/appraise** and include some text or an attachment in your message",
                                inline=False)
        welcome_embed.add_field(name="See your profile",
                                value=f"Use **/profile** to see your balance and obtained Chummedals",
                                inline=False)
        welcome_embed.add_field(name="And do a whole lot more!",
                                value="Check out all of my commands in the slash commands list",
                                inline=False)
        self.welcome_embed = welcome_embed

    @commands.slash_command(name="help", description="Show help info", usage="help")
    async def help(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        self.welcome_embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.followup.send(embed=self.welcome_embed)


def setup(bot):
    bot.add_cog(Help(bot))
