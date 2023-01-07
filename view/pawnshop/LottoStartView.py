import discord
from discord.ui import Item

from util.database import user_actions
from util.pawnshop.lottodetails import LottoDetails


class LottoStartView(discord.ui.View):
    def __init__(self, *items: Item, lotto: LottoDetails, betting_window_sec, run_lotto_callback):
        super().__init__(*items, timeout=betting_window_sec, disable_on_timeout=True)
        self.lotto = lotto
        self.betting_window_sec = betting_window_sec
        self.run_lotto_callback = run_lotto_callback

    async def on_timeout(self):
        # for child in self.children:
        #     child.disabled = True
        #     child.label = "No more bets!"

        await self.run_lotto_callback(self.lotto)

    @discord.ui.button(label="Join", style=discord.ButtonStyle.blurple)
    async def join_lotto_callback(self, button, interaction: discord.Interaction):
        if any(player.id == interaction.user.id for player in self.lotto.players):
            await interaction.response.send_message(
                f"{interaction.user.mention} You're already in this Chumlottery!"
            )
            return

        if user_actions.get_balance(interaction.user) < self.lotto.bet:
            await interaction.response.send_message(
                f"{interaction.user.mention} You're don't have enough money to join this Chumlottery!"
            )
            return

        self.lotto.players.append(interaction.user)
        await interaction.response.edit_message(
            content=self.lotto.message(),
            view=self
        )
