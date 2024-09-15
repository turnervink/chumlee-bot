import discord
from discord.ext import commands

from util.database import guild_actions


class ChannelBind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="allowchannel", description="Allow the bot to be used in a channel "
                                                             "(run in the channel you want to add)",
                            usage="allowchannel")
    async def allow_channel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        await ctx.defer()
        guild_actions.add_allowed_channel(ctx.guild.id, channel.id)
        await ctx.followup.send(f"Added {channel.mention} to the list of allowed channels")

    @commands.slash_command(name="disallowchannel", description="Disallow the bot from being used in a channel "
                                                                "(run in the channel you want to remove)",
                            usage="disallowchannel")
    async def disallow_channel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        await ctx.defer
        guild_actions.remove_allowed_channel(ctx.guild.id, channel.id)
        await ctx.followup.send(f"Removed {channel.mention} from the list of allowed channels")

    @commands.slash_command(name="allowedchannels", description="See what channels the bot is allowed to be used in",
                            usage="allowedchannels")
    async def get_allowed_channels(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        response = "You can interact with me in the following channels:\n\n"

        channel_ids = guild_actions.get_allowed_channels(ctx.guild.id)
        try:
            for channel_id in channel_ids:
                channel = self.bot.get_channel(int(channel_id))
                if channel is None:
                    guild_actions.remove_allowed_channel(ctx.guild.id, channel_id)
                else:
                    response += f"{channel.mention}\n"

            await ctx.followup.send(response)
        except TypeError:
            await ctx.followup.send("There's no allowed channels in this server. You can add one with **.allowchannel**.")


def setup(bot: commands.Bot):
    bot.add_cog(ChannelBind(bot))
