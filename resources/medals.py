paper = {
    "price": 250,
    "profile_xy": (9, 80)
}

chocolate = {
    "price": 500,
    "profile_xy": (83, 80)
}

wood = {
    "price": 1000,
    "profile_xy": (157, 80)
}

tin = {
    "price": 2000,
    "profile_xy": (231, 80)
}

bronze = {
    "price": 3500,
    "profile_xy": (9, 9)
}

silver = {
    "price": 10000,
    "profile_xy": (83, 9)
}

gold = {
    "price": 100000,
    "profile_xy": (157, 9)
}

platinum = {
    "price": 500000,
    "profile_xy": (231, 9)
}

localnames = locals()


def get_medal_price(medal):
    try:
        return localnames[medal]["price"]
    except KeyError:
        return None
