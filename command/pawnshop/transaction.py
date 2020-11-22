from asyncio import TimeoutError, sleep

import discord
from discord.ext import commands

from command.check import checks
from util.database import transaction_actions, cooldown_actions
from util.pawnshop.appraisal import Appraisal
from util import emoji


class Transaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='appraise', description='Have Chumlee appraise an item')
    @checks.user_registered()
    @checks.user_not_in_deal()
    @checks.user_not_in_cooldown()
    @checks.message_has_item_to_appraise()
    async def appraise(self, ctx: commands.Context, *, item=None):
        appraisal = Appraisal()

        if appraisal.offer > 0:
            response = (f"{appraisal.offer_message}"
                        "\n\n"
                        f"{ctx.message.author.mention} How's {appraisal.offer} {emoji.CHUMCOIN} sound?")
            await ctx.send(response)

            try:
                reply = await self.bot.wait_for('message', check=is_transaction_reply(ctx.message.author), timeout=60)

                if reply.content.lower() == "deal":
                    response = ("Alright! I'll meet you over there and do some paperwork."
                                "\n\n"
                                f"{emoji.CHUMLEE} {emoji.ARROW_RIGHT} {appraisal.offer} {emoji.CHUMCOIN} "
                                f"{emoji.ARROW_RIGHT} {ctx.message.author.mention}")
                    await ctx.send(response)

                    transaction_actions.deposit(ctx.message.author, appraisal.offer)
                    cooldown_actions.update_cooldown_end_time(ctx.message.author)
                elif reply.content.lower() == "no deal":
                    response = ("Okay, no deal then."
                                "\n\n"
                                f"{ctx.message.author.mention} No deal {emoji.NO_ENTRY}")
                    await ctx.send(response)

                    cooldown_actions.update_cooldown_end_time(ctx.message.author)
            except TimeoutError:
                response = ("Well, you snooze you lose!"
                            "\n\n"
                            f"{ctx.message.author.mention} Too slow! No deal {emoji.NO_ENTRY}")
                await ctx.send(response)
        else:
            response = ("Sorry, no can do."
                        "\n\n"
                        f"{ctx.message.author.mention} No deal {emoji.NO_ENTRY}")
            await ctx.send(response)


def is_transaction_reply(original_author: discord.User):
    def check(msg: discord.Message):
        return msg.author == original_author and (msg.content.lower() == "deal" or msg.content.lower() == "no deal")
    return check


def setup(bot: commands.Bot):
    bot.add_cog(Transaction(bot))
