tin = 2000
bronze = 3500
silver = 10000
gold = 100000
platinum = 500000


def get_medal_price(medal):
    if medal == "tin":
        return tin
    elif medal == "bronze":
        return bronze
    elif medal == "silver":
        return silver
    elif medal == "gold":
        return gold
    elif medal == "platinum":
        return platinum
    else:
        return None
