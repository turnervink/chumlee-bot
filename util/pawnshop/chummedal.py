from command.error import errors


class Chummedal:
    VALID_MEDALS = [
        "paper",
        "chocolate",
        "wood",
        "tin",
        "bronze",
        "silver",
        "gold",
        "platinum"
    ]

    MEDAL_DATA = {
        "paper": {
            "price": 250,
            "profile_xy": (42, 575)
        },
        "chocolate": {
            "price": 500,
            "profile_xy": (279, 575)
        },
        "wood": {
            "price": 1000,
            "profile_xy": (516, 575)
        },
        "tin": {
            "price": 2000,
            "profile_xy": (751, 575)
        },
        "bronze": {
            "price": 3500,
            "profile_xy": (42, 345)
        },
        "silver": {
            "price": 10000,
            "profile_xy": (279, 345)
        },
        "gold": {
            "price": 100000,
            "profile_xy": (515, 345)
        },
        "platinum": {
            "price": 500000,
            "profile_xy": (751, 345)
        }
    }

    def __init__(self, name):
        if name not in self.VALID_MEDALS:
            raise errors.InvalidMedalNameError(name)
        else:
            self.name = name
            self.image_path = f"resources/{self.name}.png"
            self.price = self.MEDAL_DATA[self.name]["price"]
            self.profile_xy = self.MEDAL_DATA[self.name]["profile_xy"]
