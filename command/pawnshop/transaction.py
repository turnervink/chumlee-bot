from discord.ext import commands

from command.check import checks
from util.database import transaction_actions, cooldown_actions
from util.pawnshop.appraisal import Appraisal
from util import emoji
from command.error import errors


class Transaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deals_in_progress = {}

    @commands.command(name="appraise", description="Have Chumlee appraise an item")
    @checks.user_registered()
    @checks.user_not_in_cooldown()
    async def appraise(self, ctx: commands.Context, *, item=None):
        if ctx.message.author.id in self.deals_in_progress:
            raise errors.UserAlreadyInDealError(ctx.message.author)

        if item is None and ctx.message.attachments is None:
            raise errors.NoItemToAppraiseError(ctx.message.author)

        appraisal = Appraisal()
        self.deals_in_progress[ctx.message.author.id] = appraisal

        if appraisal.offer > 0:
            response = (f"{appraisal.offer_message}"
                        "\n\n"
                        f"{ctx.message.author.mention} How's {appraisal.offer} {emoji.CHUMCOIN} sound?"
                        "\n\n"
                        f"{self.bot.command_prefix}deal / {self.bot.command_prefix}nodeal")
            await ctx.send(response)
        else:
            response = ("Sorry, no can do."
                        "\n\n"
                        f"{ctx.message.author.mention} No deal {emoji.NO_ENTRY}")
            await ctx.send(response)
            self.deals_in_progress.pop(ctx.message.author.id)

    @commands.command(name="deal", description="Accept an offer")
    @checks.user_registered()
    async def deal(self, ctx: commands.Context):
        if ctx.message.author.id in self.deals_in_progress:
            appraisal = self.deals_in_progress[ctx.message.author.id]

            response = ("Alright! I'll meet you over there and do some paperwork."
                        "\n\n"
                        f"{emoji.CHUMLEE} {emoji.ARROW_RIGHT} {appraisal.offer} {emoji.CHUMCOIN} "
                        f"{emoji.ARROW_RIGHT} {ctx.message.author.mention}")
            await ctx.send(response)

            transaction_actions.deposit(ctx.message.author, appraisal.offer)
            cooldown_actions.update_cooldown_end_time(ctx.message.author)
            self.deals_in_progress.pop(ctx.message.author.id)

    @commands.command(name="nodeal", description="Reject an offer")
    @checks.user_registered()
    async def nodeal(self, ctx: commands.Context):
        if ctx.message.author.id in self.deals_in_progress:
            response = ("Okay, no deal then."
                        "\n\n"
                        f"{ctx.message.author.mention} No deal {emoji.NO_ENTRY}")
            await ctx.send(response)

            cooldown_actions.update_cooldown_end_time(ctx.message.author)
            self.deals_in_progress.pop(ctx.message.author.id)


def setup(bot: commands.Bot):
    bot.add_cog(Transaction(bot))
