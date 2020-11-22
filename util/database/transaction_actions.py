from .config import db
from util.database.error.errors import *

import discord


def withdraw(user: discord.User, amount: int):
    balance = db.child('users').child(user.id).child('balance').get().val()
    if amount > balance:
        raise InsufficientFundsError(user)

    db.child('users').child(user.id).child('balance').set(balance - amount)


def deposit(user: discord.User, amount: int):
    balance = db.child('users').child(user.id).child('balance').get().val()
    db.child('users').child(user.id).child('balance').set(balance + amount)
