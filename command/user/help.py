import discord
from discord.ext import commands

from util.emoji import CHUMCOIN


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        p = self.bot.command_prefix
        welcome_embed = discord.Embed(title="Hi! I'm Chumlee, and I run this pawnshop.", colour=discord.Colour(0xffffff),
                              description="I'm here to appraise your memes, jokes, and anything else you can "
                                          f"think of. I'll offer you Chumcoins {CHUMCOIN} in exhange, and the more "
                                          "you collect the more you'll level up. You can trade in your Chumcoins "
                                          f"{CHUMCOIN} for different Chummedals to display on your profile.")
        welcome_embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/430116913797136384/785220324241047583/"
                "rs_600x600-140313141217-600.chumlee-pawn-stars.ls.31314.jpg")
        welcome_embed.add_field(name="Register a channel",
                                value=f"Use **{p}allowchannel** so I can interact with people there",
                                inline=False)
        welcome_embed.add_field(name="Get an appraisal",
                                value=f"Use **{p}appraise** and include some text or an attachment in your message",
                                inline=False)
        welcome_embed.add_field(name="See your profile",
                                value=f"Use **{p}profile** to see your balance and obtained Chummedals",
                                inline=False)
        welcome_embed.add_field(name="View a list of commands", value=f"Use **{p}commands** to see what I can do",
                                inline=False)
        self.welcome_embed = welcome_embed

    @commands.command(name="help", description="Show help info", usage="help")
    async def help(self, ctx):
        async with ctx.typing():
            await ctx.send(embed=self.welcome_embed)

    @commands.command(name="commands", description="List all commands", usage="commands")
    async def commands(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(title="Commands", colour=discord.Colour(0xffffff))
            for command in self.bot.commands:
                if not command.hidden:
                    embed.add_field(name=f"{self.bot.command_prefix}{command.usage}",
                                    value=f"{command.description}", inline=False)

            await ctx.send(embed=embed)


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))
