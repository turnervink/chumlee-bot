import discord

import re

INSULTS = [
    "fuc?k you",
    "fuc?k u",
    "whore",
    "bitch",
    "bastard",
    "motherfucker",
    "coward",
    "what the fuc?k\??"
]

RESPONSES = [
    "Well that's not very nice {}!",
    "Hey, be nice {}!",
    "Sorry {}, but you don't have to be like that!",
    "There's no need for that kind of language {}!",
    "There's no need to be rude, {}!"
]


def message_has_insult(msg: discord.Message, offerer: discord.User):
    return msg.author == offerer and any(re.search(pattern, msg.content.lower()) for pattern in INSULTS)
