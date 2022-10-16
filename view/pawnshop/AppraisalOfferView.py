import random

import discord
from discord.ui import Item

from util import emoji
from util.database import transaction_actions, user_actions, cooldown_actions
from util.pawnshop.appraisal import Appraisal, ACCEPTED_OFFER_QUOTES, REJECTED_OFFER_QUOTES, MAX_NODEAL_BEFORE_COOLDOWN


class AppraisalOfferView(discord.ui.View):
    def __init__(self, *items: Item, appraisal: Appraisal, deals_in_progress, offer_rejections):
        super().__init__(*items)
        self.appraisal = appraisal
        self.deals_in_progress = deals_in_progress
        self.offer_rejections = offer_rejections

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.appraisal.user.id == interaction.user.id

    def update_cooldown(self):
        cooldown_actions.update_cooldown_end_time(self.appraisal.user, self.appraisal.timestamp)

    @discord.ui.button(label="Deal", style=discord.ButtonStyle.green)
    async def accept_offer_callback(self, button, interaction: discord.Interaction):
        transaction_actions.deposit(self.appraisal.user, self.appraisal.offer)
        user_actions.increment_total_earnings(self.appraisal.user, self.appraisal.offer)
        self.update_cooldown()
        self.deals_in_progress.pop(self.appraisal.user.id)

        response = (f"{random.choice(ACCEPTED_OFFER_QUOTES)}"
                    "\n\n"
                    f"{emoji.CHUMLEE} {emoji.ARROW_RIGHT} {self.appraisal.offer} {emoji.CHUMCOIN} {emoji.ARROW_RIGHT} {self.appraisal.user.mention}")

        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content=response, view=self)

    @discord.ui.button(label="No deal", style=discord.ButtonStyle.red)
    async def reject_offer_callback(self, button, interaction: discord.Interaction):
        if self.appraisal.user.id in self.offer_rejections:
            rejection_count = self.offer_rejections[self.appraisal.user.id]
            if rejection_count == MAX_NODEAL_BEFORE_COOLDOWN:
                self.update_cooldown()
                self.offer_rejections.pop(self.appraisal.user.id)
            else:
                self.offer_rejections[self.appraisal.user.id] = rejection_count + 1
        else:
            self.offer_rejections[self.appraisal.user.id] = 1

        self.deals_in_progress.pop(self.appraisal.user.id)

        response = (f"{random.choice(REJECTED_OFFER_QUOTES)}"
                    "\n\n"
                    f"{self.appraisal.user.mention} No deal {emoji.NO_ENTRY}")

        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content=response, view=self)
