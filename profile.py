from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io
import requests

from dbfunctions import get_medals
from dbfunctions import get_balance

from resources import medals


def gen_profile(user):
    """
    Generates a profile display image for a user.

    :param user: the User object to generate a profile for
    :return: a byte array containing the profile image data
    """
    bg = Image.open("resources/img/chumprofile.png")
    avatar = Image.open(io.BytesIO(requests.get(user.avatar_url).content))
    avatar = avatar.resize((64, 64))

    medallist = get_medals(user)

    # Paste all of the user's medals on the profile
    if medallist is not None:
        for medal in medallist:
            try:
                im = Image.open("resources/img/medals/" + medal + "chum64.png")
                box = getattr(medals, medal)
                bg.paste(im, box=box["profile_xy"])
                im.close()
            except FileNotFoundError:
                print("No medal file found for " + medal)

    # Paste the user's avatar onto the profile
    bg.paste(avatar, box=(9, 3))

    # Draw the user's display name and coin balance on the profile
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("resources/Roboto-Regular.ttf", 24)
    smallfont = ImageFont.truetype("resources/Roboto-Regular.ttf", 18)
    draw.text((83, 3), user.display_name, (255, 255, 255), font=font)
    draw.text((108, 44), str(get_balance(user)), (255, 255, 255), font=smallfont)

    imgbytearr = io.BytesIO()
    bg.save(imgbytearr, format="PNG")
    imgbytearr = imgbytearr.getvalue()
    bg.close()

    return imgbytearr
