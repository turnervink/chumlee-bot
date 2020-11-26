from .config import db
from .error.errors import *
from util.pawnshop.medal import Medal
from util.pawnshop.level import Level


def get_user(user: discord.User):
    db_record = db.child("users").child(user.id).get().val()
    if db_record is None:
        raise UserNotFoundError(user)
    else:
        return db_record


def register(user: discord.User):
    db.child("users").child(user.id).set(NEW_USER_DATA)


def is_registered(user: discord.User) -> bool:
    record = db.child("users").child(user.id).get()

    return record.val() is not None


def get_balance(user: discord.User) -> int:
    return db.child("users").child(user.id).child("balance").get().val()


def get_medals(user: discord.User):
    try:
        medals = db.child("users").child(user.id).child("medals").order_by_value().equal_to(True).get().val()
    except IndexError:
        return None

    return medals


def award_medal(user: discord.User, medal: Medal):
    db.child("users").child(user.id).child("medals").child(medal.name).set(True)


def user_will_level_up(user: discord.User, new_deposit: int):
    current_total = get_total_earnings(user)
    current_level = Level(current_total)
    potential_new_level = Level(current_total + new_deposit)

    if current_level.title != potential_new_level.title:
        return True

    return False


def get_total_earnings(user: discord.User):
    earnings = db.child("users").child(user.id).child("totalEarnings").get().val()
    if earnings is None:
        db.child("users").child(user.id).child("totalEarnings").set(0)
        return 0

    return earnings


def increment_total_earnings(user: discord.User, amt: int):
    current_total = get_total_earnings(user)

    if current_total is None:
        current_total = 0

    db.child("users").child(user.id).child("totalEarnings").set(current_total + amt)


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
