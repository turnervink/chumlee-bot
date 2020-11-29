from .config import db, db_root
from util.database.error.errors import *

import discord


def withdraw(user: discord.User, amount: int):
    balance = db.reference(f"{db_root}/users/{user.id}/balance").get()
    if amount > balance:
        raise InsufficientFundsError(user)

    db.reference(f"{db_root}/users/{user.id}/balance").set(balance - amount)


def deposit(user: discord.User, amount: int):
    balance = db.reference(f"{db_root}/users/{user.id}/balance").get()
    db.reference(f"{db_root}/users/{user.id}/balance").set(balance + amount)
