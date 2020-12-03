from discord.ext import commands


class UserNotRegisteredError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f'You need to use .register first {user.mention}'
        super().__init__(message=message, *args)


class UserAlreadyRegisteredError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f'Looks like you\'re already registered {user.mention}!'
        super().__init__(message=message, *args)


class UserAlreadyInDealError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f'Looks like you\'ve already got a deal on the table {user.mention}!'
        super().__init__(message=message, *args)


class TransactionUsersAreEqualError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f'You can\'t pay yourself Chumcoins {user.mention}!'
        super().__init__(message=message, *args)


class NoItemToAppraiseError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f'{user.mention} you must include an attachment or some text to appraise'
        super().__init__(message=message, *args)


class InvalidChannelError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f"{user.mention} this channel can't be used for commands!"
        super().__init__(message=message, *args)


class InvalidMedalNameError(commands.CommandError):
    def __init__(self, invalid_name, *args):
        self.invalid_name = invalid_name
        message = f'{invalid_name} is not a valid medal name'
        super().__init__(message=message, *args)


class LevelNotFoundError(commands.CommandError):
    def __init__(self, value, *args):
        self.value = value
        message = f"No level found for earnings value {value}"
        super().__init__(message=message, *args)


class LottoInProgressError(commands.CommandError):
    def __init__(self):
        message = f"A lottery is already in progress!"
        super().__init__(message=message)


class NoLottoInProgressError(commands.CommandError):
    def __init__(self):
        message = f"There's no lottery in progress!"
        super().__init__(message=message)


class UserAlreadyInLottoError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f"You've already bet in this Chumlottery {user.mention}!"
        super().__init__(message=message)
