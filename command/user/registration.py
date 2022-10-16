from discord.ext import bridge, commands

from command.check import checks
from util.database import user_actions


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="register", description="Register yourself to sell at the pawnshop", usage="register")
    @checks.user_not_registered()
    async def register(self, ctx: bridge.BridgeApplicationContext):
        await ctx.defer()
        user_actions.register(ctx.author)
        await ctx.send(f"You're all set, now let's make a deal!")


def setup(bot: commands.Bot):
    bot.add_cog(Registration(bot))
