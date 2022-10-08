import random

import discord
from discord.ui import Item

from util import emoji
from util.database import transaction_actions, user_actions, cooldown_actions
from util.pawnshop.appraisal import Appraisal, ACCEPTED_OFFER_QUOTES, REJECTED_OFFER_QUOTES


class AppraisalOfferView(discord.ui.View):
    def __init__(self, *items: Item, appraisal: Appraisal):
        super().__init__(*items)
        self.appraisal = appraisal

    def update_cooldown(self):
        cooldown_actions.update_cooldown_end_time(self.appraisal.user, self.appraisal.timestamp)

    @discord.ui.button(label="Deal", style=discord.ButtonStyle.green)
    async def accept_offer_callback(self, button, interaction: discord.Interaction):
        transaction_actions.deposit(self.appraisal.user, self.appraisal.offer)
        user_actions.increment_total_earnings(self.appraisal.user, self.appraisal.offer)
        self.update_cooldown()
        user_actions.set_is_in_deal(self.appraisal.user, self.appraisal.guild, False)

        response = (f"{random.choice(ACCEPTED_OFFER_QUOTES)}"
                    "\n\n"
                    f"{emoji.CHUMLEE} {emoji.ARROW_RIGHT} {self.appraisal.offer} {emoji.CHUMCOIN}")

        await interaction.response.send_message(response)

    @discord.ui.button(label="No deal", style=discord.ButtonStyle.red)
    async def reject_offer_callback(self, button, interaction):
        # TODO Track rejection count in the database
        self.update_cooldown()
        user_actions.set_is_in_deal(self.appraisal.user, self.appraisal.guild, False)

        response = (f"{random.choice(REJECTED_OFFER_QUOTES)}"
                    "\n\n"
                    f"{self.appraisal.user.mention} No deal {emoji.NO_ENTRY}")

        await interaction.response.send_message(response)
