import discord
from discord.ext import commands


class UserNotFoundError(commands.CommandError):
    def __init__(self, user: discord.User, *args):
        self.user = user
        message = f'User {user.mention} is not registered with the pawnshop'
        super().__init__(message=message, *args)


class InsufficientFundsError(commands.CommandError):
    def __init__(self, user: discord.User, *args):
        self.user = user
        message = f'{user.mention} has insufficient funds for this transaction'
        super().__init__(message=message, *args)