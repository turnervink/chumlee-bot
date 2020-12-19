import discord
from discord.ext import commands
from asyncio import TimeoutError

from command.check import checks
from util.pawnshop import cyberbullying
from util.database import transaction_actions, cooldown_actions, user_actions
from util.pawnshop.appraisal import Appraisal, ACCEPTED_OFFER_QUOTES, REJECTED_OFFER_QUOTES
from util.pawnshop.level import Level
from util import emoji, analytics
from error import errors

import random


class Transaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.analytics = analytics.Analytics()
        self.deals_in_progress = {}
        self.offer_rejections = {}

    @commands.command(name="appraise", description="Have Chumlee appraise an item",
                      usage="appraise <some text or an attachment>")
    @checks.user_not_in_cooldown()
    @checks.user_registered()
    async def appraise(self, ctx: commands.Context, *, item=None):
        await self.analytics.send_event(category="command", action="appraise")

        async with ctx.message.channel.typing():
            if ctx.message.author.id in self.deals_in_progress:
                raise errors.UserAlreadyInDealError(ctx.message.author)

            if item is None and not ctx.message.attachments:
                raise errors.NoItemToAppraiseError(ctx.message.author)

            if item == f"<@!{self.bot.user.id}>":
                await ctx.send(f"I'm all about self love {ctx.message.author.mention}, so I'll give myself a 10/10!")
                return

            appraisal = Appraisal()
            self.deals_in_progress[ctx.message.author.id] = appraisal

            if appraisal.offer > 0:
                response = (f"{appraisal.offer_message}"
                            "\n\n"
                            f"{ctx.message.author.mention} How's {appraisal.offer} {emoji.CHUMCOIN} sound?"
                            "\n\n"
                            f"{self.bot.command_prefix}deal / {self.bot.command_prefix}nodeal")
                await ctx.send(response)

                try:
                    await self.bot.wait_for("message",
                                            check=lambda m: cyberbullying.message_has_insult(m, ctx.message.author),
                                            timeout=10)
                    await ctx.send(random.choice(cyberbullying.RESPONSES).format(ctx.message.author.mention))
                except TimeoutError:
                    pass
            else:
                response = (f"{appraisal.offer_message}"
                            "\n\n"
                            f"{ctx.message.author.mention} No deal {emoji.NO_ENTRY}")
                await ctx.send(response)
                self.deals_in_progress.pop(ctx.message.author.id)

    @commands.command(name="deal", description="Accept an offer", hidden=True)
    @checks.user_registered()
    async def deal(self, ctx: commands.Context):
        async with ctx.message.channel.typing():
            if ctx.message.author.id in self.deals_in_progress:
                appraisal = self.deals_in_progress[ctx.message.author.id]

                response = (f"{random.choice(ACCEPTED_OFFER_QUOTES)}"
                            "\n\n"
                            f"{emoji.CHUMLEE} {emoji.ARROW_RIGHT} {appraisal.offer} {emoji.CHUMCOIN} "
                            f"{emoji.ARROW_RIGHT} {ctx.message.author.mention}")
                await ctx.send(response)

                transaction_actions.deposit(ctx.message.author, appraisal.offer)
                did_level_up = user_actions.user_will_level_up(ctx.message.author, appraisal.offer)
                user_actions.increment_total_earnings(ctx.message.author, appraisal.offer)
                cooldown_actions.update_cooldown_end_time(ctx.message.author, appraisal.timestamp)
                self.deals_in_progress.pop(ctx.message.author.id)
                await self.analytics.send_event(category="offer_response", action="accept", value=appraisal.offer)

                if did_level_up:
                    level = Level(user_actions.get_total_earnings(ctx.message.author))
                    embed = discord.Embed(title="Level Up! <:chumlee:337842115931537408> :tada:",
                                          colour=discord.Colour(0xf1c40f),
                                          description=f"**Congratulations {ctx.message.author.mention}, "
                                                      f"you levelled up!** \n\n You're now a {level.title}!")

                    embed.set_thumbnail(url=ctx.message.author.avatar_url)
                    embed.set_footer(text="Keep levelling up by selling more stuff to Chumlee!")

                    await ctx.send(embed=embed)

    @commands.command(name="nodeal", description="Reject an offer", hidden=True)
    @checks.user_registered()
    async def nodeal(self, ctx: commands.Context):
        async with ctx.message.channel.typing():
            if ctx.message.author.id in self.deals_in_progress:
                appraisal = self.deals_in_progress[ctx.message.author.id]

                response = (f"{random.choice(REJECTED_OFFER_QUOTES)}"
                            "\n\n"
                            f"{ctx.message.author.mention} No deal {emoji.NO_ENTRY}")
                await ctx.send(response)

                if ctx.message.author.id in self.offer_rejections:
                    rejection_count = self.offer_rejections[ctx.message.author.id]
                    if rejection_count == 2:
                        cooldown_actions.update_cooldown_end_time(ctx.message.author, appraisal.timestamp)
                        self.offer_rejections.pop(ctx.message.author.id)
                    else:
                        self.offer_rejections[ctx.message.author.id] = rejection_count + 1
                else:
                    self.offer_rejections[ctx.message.author.id] = 1

                self.deals_in_progress.pop(ctx.message.author.id)
                await self.analytics.send_event(category="offer_response", action="reject", value=appraisal.offer)

    @commands.command(name="cooldown", description="See how much longer you have left in your cooldown",
                      usage="cooldown")
    @checks.user_registered()
    async def cooldown(self, ctx: commands.Context):
        await self.analytics.send_event(category="command", action="cooldown")

        async with ctx.message.channel.typing():
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
    bot.add_cog(Transaction(bot))
