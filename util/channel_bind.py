from discord.ext import commands

from util.database import guild_actions


class ChannelBind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="allowchannel", description="Allow the bot to be used in a channel "
                                                       "(run in the channel you want to add)",
                      usage="allowchannel")
    async def allow_channel(self, ctx: commands.Context):
        guild_actions.add_allowed_channel(ctx.guild.id, ctx.message.channel.id)
        await ctx.send(f"Added {ctx.channel.mention} to the list of allowed channels")

    @commands.command(name="disallowchannel", description="Disallow the bot from being used in a channel "
                                                          "(run in the channel you want to remove)",
                      usage="disallowchannel")
    async def disallow_channel(self, ctx: commands.Context):
        guild_actions.remove_allowed_channel(ctx.guild.id, ctx.message.channel.id)
        await ctx.send(f"Removed {ctx.channel.mention} from the list of allowed channels4")

    @commands.command(name="allowedchannels", description="See what channels the bot is allowed to be used in",
                      usage="allowedchannels")
    async def get_allowed_channels(self, ctx: commands.Context):
        response = "You can interact with me in the following channels:\n\n"

        channel_ids = guild_actions.get_allowed_channels(ctx.guild.id)
        try:
            for channel_id in channel_ids:
                channel = self.bot.get_channel(int(channel_id))
                if channel is None:
                    guild_actions.remove_allowed_channel(ctx.guild.id, channel_id)
                else:
                    response += f"{channel.mention}\n"

            await ctx.send(response)
        except TypeError:
            await ctx.send("There's no allowed channels in this server. You can add one with **.allowchannel**.")


def setup(bot: commands.Bot):
    bot.add_cog(ChannelBind(bot))
