from .config import db
from .error.errors import *
from util.pawnshop.medal import Medal


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


def get_level(user: discord.User):
    return db.child("users").child(user.id).child("level").get().val()


def set_level(user: discord.User, new_level: int):
    db.child("users").child(user.id).child("level").set(new_level)


NEW_USER_DATA = {
    "balance": 20,
    "level": 1,
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
