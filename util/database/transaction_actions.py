from .config import db
from util.database import user_actions
from command.error.errors import *
from util.database.error.errors import *
from util.emoji import CHUMCOIN

import discord


def transfer(payer: discord.User, payee: discord.User, amount: int) -> str:
    if payer == payee:
        raise TransactionUsersAreEqualError(payer)

    if not user_actions.is_registered(payee):
        raise UserNotRegisteredError(payee)

    withdraw(payer, amount)
    deposit(payee, amount)

    return f'{payer.mention} paid {payee.mention} {amount} {CHUMCOIN}'


def withdraw(user: discord.User, amount: int) -> None:
    balance = db.child('users').child(user.id).child('balance').get().val()
    if amount > balance:
        raise InsufficientFundsError(user)

    db.child('users').child(user.id).child('balance').set(balance - amount)


def deposit(user: discord.User, amount: int) -> None:
    balance = db.child('users').child(user.id).child('balance').get().val()
    db.child('users').child(user.id).child('balance').set(balance + amount)
