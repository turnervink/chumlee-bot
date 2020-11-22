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
        message = f'{user.mention} only #the-pawnshop can be used for commands!'
        super().__init__(message=message, *args)
