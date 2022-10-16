import random
from asyncio import TimeoutError

import discord
from discord.ext import commands

from command.check import checks
from error import errors
from util import emoji
from util.database import cooldown_actions, user_actions
from util.pawnshop import cyberbullying
from util.pawnshop.appraisal import Appraisal
from view.pawnshop.AppraisalOfferView import AppraisalOfferView

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
    @checks.user_not_in_cooldown()
    @checks.user_registered()
    async def appraise(
            self,
            ctx: discord.ApplicationContext,
            text: discord.Option(str, required=False, default=None),
            image: discord.Option(discord.Attachment, required=False, default=None)
    ):
        await ctx.defer()

        if ctx.author.id in self.deals_in_progress:
            raise errors.UserAlreadyInDealError(ctx.author)

        if text is None and image is None:
            raise errors.NoItemToAppraiseError(ctx.author)

        if text is not None and any(blacklisted_item in text for blacklisted_item in BLACKLISTED_ITEMS) \
                or text == "again":
            await ctx.respond(f"Nice try {ctx.author.mention}, but I already took a look at that!")
            return

        if text == f"<@!{self.bot.user.id}>":
            await ctx.respond(f"I'm all about self love {ctx.author.mention}, so I'll give myself a 10/10!")
            return

        # TODO Add support for video attachments
        if image is not None and image.content_type.split("/")[0] != "image":
            await ctx.respond("That attachment doesn't look like an image file, I can only accept text or images!")
            return

        appraisal = Appraisal(ctx.author, ctx.guild, text, image)
        self.deals_in_progress[ctx.author.id] = appraisal

        offer_embed = discord.Embed(title="Let's take a look...", color=0xffffff)
        offer_embed.set_thumbnail(url=self.bot.user.avatar)

        if image is not None:
            offer_embed.set_image(url=image.url)

        if text is not None:
            offer_embed.add_field(name="Your offer", value=text, inline=False)

        await ctx.respond(embed=offer_embed)

        if appraisal.offer > 0:
            response = (f"{appraisal.offer_message}"
                        "\n\n"
                        f"{ctx.author.mention} How's {appraisal.offer} {emoji.CHUMCOIN} sound?")
            await ctx.followup.send(
                response,
                view=AppraisalOfferView(
                    appraisal=appraisal,
                    deals_in_progress=self.deals_in_progress,
                    offer_rejections=self.offer_rejections
                )
            )
        else:
            response = (f"{appraisal.offer_message}"
                        "\n\n"
                        f"{ctx.author.mention} No deal {emoji.NO_ENTRY}")
            self.deals_in_progress.pop(ctx.author.id)
            await ctx.followup.send(response)

        try:
            await self.bot.wait_for("message",
                                    check=lambda m: cyberbullying.message_has_insult(m, ctx.author),
                                    timeout=INSULT_TIME_WINDOW_SECONDS)
            await ctx.send(random.choice(cyberbullying.RESPONSES).format(ctx.author.mention))
        except TimeoutError:
            pass

    @commands.slash_command(name="cooldown", description="See how much longer you have left in your cooldown",
                            usage="cooldown")
    @checks.user_registered()
    async def cooldown(self, ctx: discord.ApplicationContext):
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
