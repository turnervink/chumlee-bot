import os

from discord.ext import commands

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    bot.load_extension('command.error.error_handlers')
    bot.load_extension('command.greetings')
    bot.load_extension('command.user.help')
    bot.load_extension('command.user.registration')
    bot.load_extension('command.user.profile')
    bot.load_extension('command.user.transaction')
    bot.load_extension('command.pawnshop.transaction')
    print('Bot ready!')

bot.run(os.environ['BOT_TOKEN'])
