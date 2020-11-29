from .config import db, db_root
from .error.errors import *
from util.pawnshop.medal import Medal
from util.pawnshop.level import Level


def get_user(user: discord.User):
    db_record = db.reference(f"{db_root}/users/{user.id}").get()
    if db_record is None:
        raise UserNotFoundError(user)
    else:
        return db_record


def register(user: discord.User):
    db.reference(f"{db_root}/users/{user.id}").set(NEW_USER_DATA)


def is_registered(user: discord.User):
    record = db.reference(f"{db_root}/users/{user.id}").get()

    return record is not None


def get_balance(user: discord.User):
    return db.reference(f"{db_root}/users/{user.id}/balance").get()


def get_medals(user: discord.User):
    try:
        medals = db.reference(f"{db_root}/users/{user.id}/medals").order_by_value().equal_to(True).get()
    except IndexError:
        return None

    return medals


def award_medal(user: discord.User, medal: Medal):
    db.reference(f"{db_root}/users/{user.id}/medals/{medal.name}").set(True)


def user_will_level_up(user: discord.User, new_deposit: int):
    current_total = get_total_earnings(user)
    current_level = Level(current_total)
    potential_new_level = Level(current_total + new_deposit)

    if current_level.title != potential_new_level.title:
        return True

    return False


def get_total_earnings(user: discord.User):
    earnings = db.reference(f"{db_root}/users/{user.id}/totalEarnings").get()
    if earnings is None:
        db.reference(f"{db_root}/users/{user.id}/totalEarnings").set(0)
        return 0

    return earnings


def increment_total_earnings(user: discord.User, amt: int):
    current_total = get_total_earnings(user)

    if current_total is None:
        current_total = 0

    db.reference(f"{db_root}/users/{user.id}/totalEarnings").set(current_total + amt)


def get_level(user: discord.User):
    earnings = get_total_earnings(user)
    return Level(earnings)


NEW_USER_DATA = {
    "balance": 20,
    "totalEarnings": 0,
    "medals": {
        "paper": False,
        "chocolate": False,
        "wood": False,
        "tin": False,
        "bronze": False,
        "silver": False,
        "gold": False,
        "platinum": False
    }
}
