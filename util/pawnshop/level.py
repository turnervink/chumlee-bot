def total_earnings_is_between(earnings: int, values: (int, int)):
    low, high = values
    return low <= earnings < high


def find_level_data(earnings: int):
    for level_data in LEVEL_DATA:
        if total_earnings_is_between(earnings, level_data["range"]):
            return level_data

    return None


class Level:
    def __init__(self, user_total_earnings: int):
        level_data = find_level_data(user_total_earnings)

        if level_data is None:
            level_data = LEVEL_DATA[-1]

        self.title = level_data["title"]
        self.required_earnings = level_data["range"]


LEVEL_DATA = [
    {
        "title": "Chumbebbie",
        "range": (0, 5000)
    },
    {
        "title": "Chumpeddler",
        "range": (5000, 20_000)
    },
    {
        "title": "Chumtrader",
        "range": (20_000, 65_000)
    },
    {
        "title": "Chumdealer",
        "range": (65_000, 200_000)
    },
    {
        "title": "Chumwholesaler",
        "range": (200_000, 605_000)
    }
]
