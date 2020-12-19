import discord

import re


INSULTS = [
    "fuc?k you",
    "fuc?k u",
    "whore",
    "bitch",
    "bastard",
    "motherfucker"
]

RESPONSES = [
    "Well that's not very nice {}!",
    "Hey, be nice {}!",
    "Sorry {}, but you don't have to be like that!"
]


def message_has_insult(msg: discord.Message, offerer: discord.User):
    return msg.author == offerer and any(re.search(pattern, msg.content.lower()) for pattern in INSULTS)
