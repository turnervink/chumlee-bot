import random
from asyncio import TimeoutError

import discord
from discord.ext import bridge, commands

from command.check import checks
from error import errors
from util import emoji
from util.database import cooldown_actions, user_actions
from util.pawnshop import cyberbullying
from util.pawnshop.appraisal import Appraisal
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

    @commands.slash_command(name="appraise", description="Have Chumlee appraise an item",
                            usage="appraise <some text or an attachment>")
    @checks.user_not_in_deal()
    @checks.user_not_in_cooldown()
    @checks.user_registered()
    async def appraise(
            self,
            ctx: bridge.BridgeApplicationContext,
            text: discord.Option(str, required=False, default=None),
            image: discord.Option(discord.Attachment, required=False, default=None)
    ):
        await ctx.defer()

        if text is None and image is None:
            raise errors.NoItemToAppraiseError(ctx.author)

        if text is not None and any(blacklisted_item in text for blacklisted_item in BLACKLISTED_ITEMS) \
                or text == "again":
            await ctx.respond(f"Nice try {ctx.author.mention}, but I already took a look at that!")
            return

        if text == f"<@!{self.bot.user.id}>":
            await ctx.respond(f"I'm all about self love {ctx.author.mention}, so I'll give myself a 10/10!")
            return

        appraisal = Appraisal(ctx.author, ctx.guild)
        user_actions.set_is_in_deal(ctx.author, ctx.guild, True)

        if appraisal.offer > 0:
            response = (f"{appraisal.offer_message}"
                        "\n\n"
                        f"{ctx.author.mention} How's {appraisal.offer} {emoji.CHUMCOIN} sound?")
            await ctx.respond(response, view=AppraisalOfferView(appraisal=appraisal))
        else:
            response = (f"{appraisal.offer_message}"
                        "\n\n"
                        f"{ctx.author.mention} No deal {emoji.NO_ENTRY}")
            await ctx.respond(response)

        try:
            await self.bot.wait_for("message",
                                    check=lambda m: cyberbullying.message_has_insult(m, ctx.author),
                                    timeout=INSULT_TIME_WINDOW_SECONDS)
            await ctx.respond(random.choice(cyberbullying.RESPONSES).format(ctx.author.mention))
        except TimeoutError:
            pass

    @commands.slash_command(name="cooldown", description="See how much longer you have left in your cooldown",
                      usage="cooldown")
    @checks.user_registered()
    async def cooldown(self, ctx: bridge.BridgeApplicationContext):
        await ctx.defer()
        cooldown = cooldown_actions.get_remaining_cooldown_time(ctx.author)

        if cooldown is not None:
            if cooldown < 60:
                time_remaining = f"{round(cooldown, 0)} seconds"
            else:
                minutes = round(cooldown / 60)
                time_remaining = f"{minutes} minutes" if minutes != 1 else f"{minutes} minute"

            await ctx.respond(f"You need to wait {time_remaining} until your next appraisal")
        else:
            await ctx.respond(f"You're not in a cooldown!")


def setup(bot: commands.Bot):
    bot.add_cog(PawnshopTransaction(bot))
