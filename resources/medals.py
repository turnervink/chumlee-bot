paper = {
    "price": 250,
    "profile_xy": (9, 180)
}

chocolate = {
    "price": 500,
    "profile_xy": (83, 180)
}

wood = {
    "price": 1000,
    "profile_xy": (157, 180)
}

tin = {
    "price": 2000,
    "profile_xy": (231, 180)
}

bronze = {
    "price": 3500,
    "profile_xy": (9, 109)
}

silver = {
    "price": 10000,
    "profile_xy": (83, 109)
}

gold = {
    "price": 100000,
    "profile_xy": (157, 109)
}

platinum = {
    "price": 500000,
    "profile_xy": (231, 109)
}

medalinfo = "```" \
            "Chummedal Prices:\n\n" \
            "Paper Chummedal: 250cc\n" \
            "Chocolate Chummedal: 500cc\n" \
            "Wood Chummedal: 1,000cc\n" \
            "Tin Chummedal: 2,000cc\n" \
            "Bronze Chummedal: 3,500cc\n" \
            "Silver Chummedal: 10,000cc\n" \
            "Gold Chummedal: 100,000cc\n" \
            "Platinum Chummedal: 500,000cc" \
            "```"

localnames = locals()


def get_medal_price(medal):
    try:
        return localnames[medal]["price"]
    except KeyError:
        return None
