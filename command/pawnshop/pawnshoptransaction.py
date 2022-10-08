import discord
from discord.ext import commands
from asyncio import TimeoutError

from command.check import checks
from util.pawnshop import cyberbullying
from util.database import cooldown_actions, user_actions
from util.pawnshop.appraisal import Appraisal
from util import emoji
from error import errors

import random

from view.pawnshop.AppraisalOfferView import AppraisalOfferView

MAX_NODEAL_BEFORE_COOLDOWN = 2
INSULT_TIME_WINDOW_SECONDS = 30
BLACKLISTED_ITEMS = [
    "it again",
    "it properly"
]


class PawnshopTransaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deals_in_progress = {}
        self.offer_rejections = {}

    @commands.slash_command(name="button")
    async def button_test(self, ctx: discord.ApplicationContext):
        await ctx.respond("This is a button!", view=AppraisalOfferView())

    @commands.command(name="appraise", description="Have Chumlee appraise an item",
                      usage="appraise <some text or an attachment>")
    @checks.user_not_in_deal()
    @checks.user_not_in_cooldown()
    @checks.user_registered()
    async def appraise(self, ctx: commands.Context, *, item=None):
        async with ctx.typing():
            if item is None and not ctx.message.attachments:
                raise errors.NoItemToAppraiseError(ctx.message.author)

            if item is not None and any(blacklisted_item in item for blacklisted_item in BLACKLISTED_ITEMS) \
                    or item == "again":
                await ctx.send(f"Nice try {ctx.message.author.mention}, but I already took a look at that!")
                return

            if item == f"<@!{self.bot.user.id}>":
                await ctx.send(f"I'm all about self love {ctx.message.author.mention}, so I'll give myself a 10/10!")
                return

            appraisal = Appraisal(ctx.message.author, ctx.message.guild)
            user_actions.set_is_in_deal(ctx.message.author, ctx.message.guild, True)

            if appraisal.offer > 0:
                response = (f"{appraisal.offer_message}"
                            "\n\n"
                            f"{ctx.message.author.mention} How's {appraisal.offer} {emoji.CHUMCOIN} sound?")
                await ctx.send(response, view=AppraisalOfferView(appraisal=appraisal))
            else:
                response = (f"{appraisal.offer_message}"
                            "\n\n"
                            f"{ctx.message.author.mention} No deal {emoji.NO_ENTRY}")
                await ctx.send(response)

            try:
                await self.bot.wait_for("message",
                                        check=lambda m: cyberbullying.message_has_insult(m, ctx.message.author),
                                        timeout=INSULT_TIME_WINDOW_SECONDS)
                await ctx.send(random.choice(cyberbullying.RESPONSES).format(ctx.message.author.mention))
            except TimeoutError:
                pass

    @commands.command(name="cooldown", description="See how much longer you have left in your cooldown",
                      usage="cooldown")
    @checks.user_registered()
    async def cooldown(self, ctx: commands.Context):
        async with ctx.typing():
            cooldown = cooldown_actions.get_remaining_cooldown_time(ctx.message.author)

            if cooldown is not None:
                if cooldown < 60:
                    time_remaining = f"{round(cooldown, 0)} seconds"
                else:
                    minutes = round(cooldown / 60)
                    time_remaining = f"{minutes} minutes" if minutes != 1 else f"{minutes} minute"

                await ctx.send(f"You need to wait {time_remaining} until your next appraisal {ctx.message.author.mention}")
            else:
                await ctx.send(f"You're not in a cooldown {ctx.message.author.mention}!")


def setup(bot: commands.Bot):
    bot.add_cog(PawnshopTransaction(bot))
