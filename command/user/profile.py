import aiohttp
import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io

from command.check import checks
from util.database import user_actions
from util.emoji import CHUMCOIN
from util.pawnshop.medal import Medal
from util.pawnshop.level import Level


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='profile', description='View your profile')
    @checks.user_registered()
    async def profile(self, ctx: commands.Context):
        async with ctx.message.channel.typing():
            profile_bytes = await generate_profile(ctx.message.author)
            await ctx.send(file=discord.File(io.BytesIO(profile_bytes), filename="profile.png"))

    @commands.command(name='balance', aliases=['bal'], description='Get your Chumcoin balance')
    @checks.user_registered()
    async def balance(self, ctx: commands.Context):
        balance = user_actions.get_balance(ctx.message.author)
        await ctx.send(f'{ctx.message.author.mention} your balance is {balance} {CHUMCOIN}')


async def generate_profile(user: discord.User):
    background = Image.open("resources/profile.png")

    async with aiohttp.ClientSession() as session:
        async with session.get(str(user.avatar_url)) as r:
            avatar_data = io.BytesIO(await r.read())

    # Draw the user's avatar
    avatar = Image.open(avatar_data)
    avatar = avatar.resize((225, 225))
    background.paste(avatar, box=(55, 55))

    # Draw the user's display name
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("resources/Roboto-Regular.ttf", 90)
    draw.text((305, 32), user.display_name, (255, 255, 255), font=font)

    # Draw the user's balance
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("resources/Roboto-Regular.ttf", 70)
    draw.text((406, 155), str(user_actions.get_balance(user)), (255, 255, 255), font=font)

    # Draw the user's level title
    level = Level(user_actions.get_total_earnings(user))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("resources/Roboto-Regular.ttf", 60)
    draw.text((325, 245), level.title, (255, 255, 255), font=font)

    # Fill in the user's acquired medals
    medals = user_actions.get_medals(user)

    if medals is not None:
        for m in medals:
            medal = Medal(m)
            medal_image = Image.open(medal.image_path).resize((216, 209))
            background.paste(medal_image, box=medal.profile_xy, mask=medal_image)
            medal_image.close()

    profile_bytes = io.BytesIO()
    background.save(profile_bytes, format="PNG")
    profile_bytes = profile_bytes.getvalue()
    background.close()

    return profile_bytes


def setup(bot: commands.Bot):
    bot.add_cog(Profile(bot))
