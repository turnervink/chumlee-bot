import random
import time

import discord


class Appraisal:
    def __init__(self, user: discord.User, guild: discord.Guild):
        random.seed()
        self.user = user
        self.guild = guild
        self.timestamp = int(time.time())
        self.item_tier_value = random.random()
        self.offer = self.__get_offer()
        self.offer_message = self.__get_offer_message()

    def __get_offer(self):
        if self.item_tier_value > ITEM_TIER_FIVE:
            return random.randint(500, 1000)
        elif self.item_tier_value > ITEM_TIER_FOUR:
            return random.randint(250, 500)
        elif self.item_tier_value > ITEM_TIER_THREE:
            return random.randint(100, 250)
        elif self.item_tier_value > ITEM_TIER_TWO:
            return random.randint(10, 100)
        elif self.item_tier_value > ITEM_TIER_ONE:
            return random.randint(1, 10)
        else:
            return 0

    def __get_offer_message(self):
        if self.item_tier_value > ITEM_TIER_FIVE:
            return random.choice(TIER_FIVE_QUOTES)
        elif self.item_tier_value > ITEM_TIER_FOUR:
            return random.choice(TIER_FOUR_QUOTES)
        elif self.item_tier_value > ITEM_TIER_THREE:
            return random.choice(TIER_THREE_QUOTES)
        elif self.item_tier_value > ITEM_TIER_TWO:
            return random.choice(TIER_TWO_QUOTES)
        elif self.item_tier_value > ITEM_TIER_ONE:
            return random.choice(TIER_ONE_QUOTES)
        else:
            return random.choice(TIER_ZERO_QUOTES)


MAX_NODEAL_BEFORE_COOLDOWN = 2

ITEM_TIER_ONE = 0.05
ITEM_TIER_TWO = 0.25
ITEM_TIER_THREE = 0.5
ITEM_TIER_FOUR = 0.8
ITEM_TIER_FIVE = 0.95

TIER_ZERO_QUOTES = [
    "Looks like a bunch of junk in the trunk.",
    "I don't think so man...",
    "Uhh... no.",
    "Not gonna happen.",
    "Rick would kill me if I spent money on this."
]

TIER_ONE_QUOTES = [
    "It's decent, I guess.",
    "I don't know a whole lot about it, but I guess I'll take it.",
    "I'll give you a couple bucks for it.",
    "How's a couple of bucks sound?",
    "It's not worth much, honestly."
]

TIER_TWO_QUOTES = [
    "Ehh... I've seen better but sure.",
    "Well... I guess I could make you a deal.",
    "I've seen better, but I guess I can make a deal.",
    "I can't give you much."
]

TIER_THREE_QUOTES = [
    "Sweet!",
    "Awesome!",
    "Sure!",
    "Sounds alright. Let's make a deal."
]

TIER_FOUR_QUOTES = [
    "That thing is badass!",
    "Oh man that's sick!",
    "Wow! This is definitely something I can make a deal on!",
    "Heck yeah I'll make you a deal!"
]

TIER_FIVE_QUOTES = [
    "Oh man, this is awesome!",
    "Rick would kill me if I passed up on this!",
    "This is a must buy FOR SURE!",
    "Hell yeah I can make you a deal!"
]

ACCEPTED_OFFER_QUOTES = [
    "Alright! I'll meet you over there and do some paperwork.",
    "Sick! It's a deal!",
    "Awesome! Let's make a deal!",
    "Deal!"
]

REJECTED_OFFER_QUOTES = [
    "Okay, no deal then.",
    "Alright, your loss.",
    "No deal? Alright then!",
    "Your call, man. No deal."
]
