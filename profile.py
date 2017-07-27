from PIL import Image
import io

from dbfunctions import get_medals

from resources import medals


def gen_profile(user):
    bg = Image.open("resources/img/chumprofile.png")

    medallist = get_medals(user)

    if medals is not None:
        for medal in medallist:
            try:
                im = Image.open("resources/img/medals/" + medal + "chum64.png")
                box = getattr(medals, medal)
                bg.paste(im, box=box["profile_xy"])
                im.close()
            except FileNotFoundError:
                print("No medal file found for " + medal)

    imgbytearr = io.BytesIO()
    bg.save(imgbytearr, format="PNG")
    imgbytearr = imgbytearr.getvalue()
    bg.close()

    return imgbytearr
