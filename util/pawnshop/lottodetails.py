from typing import List

import discord

from util import emoji


class LottoDetails:
    def __init__(
            self,
            bet: int,
            betting_window: int,
            guild: discord.Guild,
            starting_user: discord.User,
            channel: discord.PartialMessageable,
            players: List[discord.User]
    ):
        self.bet = bet
        self.betting_window = betting_window
        self.guild = guild
        self.starting_user = starting_user
        self.channel = channel
        self.players = players

    def message(self):
        player_mentions = (player.mention for player in self.players)
        player_list = "\n".join(player_mentions)

        egg = " Nice." if self.bet == 69 else ""
        return (f"{self.starting_user.mention} has started a Chumlottery!{egg}"
                "\n\n"
                f"Click **Join** to bet {self.bet} {emoji.CHUMCOIN} and join! Bets are open "
                f"for {self.betting_window} seconds. "
                "\n\n"
                "**Who's in**"
                "\n"
                f"{player_list}")
