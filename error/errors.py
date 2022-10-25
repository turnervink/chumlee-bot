import discord
from discord.ext import commands


class BotError(commands.CommandError):
    def __init__(self, message: str, *args):
        super().__init__(message=message, *args)


class UserNotRegisteredError(BotError):
    def __init__(self, user, *args):
        self.user = user
        message = f'You need to use **/register** first {user.mention}'
        super().__init__(message=message, *args)


class UserAlreadyRegisteredError(BotError):
    def __init__(self, user, *args):
        self.user = user
        message = f'Looks like you\'re already registered {user.mention}!'
        super().__init__(message=message, *args)


class UserAlreadyInDealError(BotError):
    def __init__(self, user, *args):
        self.user = user
        message = f'Looks like you\'ve already got a deal on the table {user.mention}!'
        super().__init__(message=message, *args)


class TransactionUsersAreEqualError(BotError):
    def __init__(self, user, *args):
        self.user = user
        message = f'You can\'t pay yourself Chumcoins {user.mention}!'
        super().__init__(message=message, *args)


class NoItemToAppraiseError(BotError):
    def __init__(self, user, *args):
        self.user = user
        message = f'{user.mention} you must include an attachment or some text to appraise'
        super().__init__(message=message, *args)


class InvalidChannelError(BotError):
    def __init__(self, user, *args):
        self.user = user
        message = f"{user.mention} this channel can't be used for commands!" \
                  f"\nYou can allow a channel using **/allowchannel**"
        super().__init__(message=message, *args)


class InvalidMedalNameError(BotError):
    def __init__(self, invalid_name, *args):
        self.invalid_name = invalid_name
        message = f'{invalid_name} is not a valid medal name'
        super().__init__(message=message, *args)


class LevelNotFoundError(BotError):
    def __init__(self, value, *args):
        self.value = value
        message = f"No level found for earnings value {value}"
        super().__init__(message=message, *args)


class LottoInProgressError(BotError):
    def __init__(self, *args):
        message = f"A lottery is already in progress!"
        super().__init__(message=message, *args)


class NoLottoInProgressError(BotError):
    def __init__(self, *args):
        message = f"There's no lottery in progress!"
        super().__init__(message=message, *args)


class UserAlreadyInLottoError(BotError):
    def __init__(self, user, *args):
        self.user = user
        message = f"You've already bet in this Chumlottery {user.mention}!"
        super().__init__(message=message, *args)


class UserNotFoundError(BotError):
    def __init__(self, user: discord.User, *args):
        self.user = user
        message = f'User {user.mention} is not registered with the pawnshop'
        super().__init__(message=message, *args)


class InsufficientFundsError(BotError):
    def __init__(self, user: discord.User, *args):
        self.user = user
        message = f'{user.mention} has insufficient funds for this transaction'
        super().__init__(message=message, *args)


class InsufficientStockError(BotError):
    def __init__(self, user: discord.User, *args):
        self.user = user
        message = f'{user.mention} has insufficient stock for this transaction'
        super().__init__(message=message, *args)
