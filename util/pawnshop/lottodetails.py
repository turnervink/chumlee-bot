from typing import List

import discord

from util import emoji


class LottoDetails:
    def __init__(self, bet: int, guild: discord.Guild, channel: discord.PartialMessageable, players: List[discord.User]):
        self.bet = bet
        self.guild = guild
        self.channel = channel
        self.players = players

    def message(self, user: discord.User, betting_window_sec: int):
        player_mentions = (player.mention for player in self.players)
        player_list = "\n".join(player_mentions)

        egg = " Nice." if self.bet == 69 else ""
        return (f"{user.mention} has started a Chumlottery!{egg}"
                "\n\n"
                f"Click **Join** to bet {self.bet} {emoji.CHUMCOIN} and join! Bets are open "
                f"for {betting_window_sec} seconds. "
                "\n\n"
                "**Who's in**"
                "\n"
                f"{player_list}")
