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


class TransactionUsersAreEqualError(commands.CommandError):
    def __init__(self, user, *args):
        self.user = user
        message = f'You can\'t pay yourself Chumcoins {user.mention}!'
        super().__init__(message=message, *args)
