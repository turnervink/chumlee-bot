from datetime import datetime, timezone

import discord

from error.errors import InsufficientStockError
from .config import db, db_root


def timestamp_key(timestamp: datetime.timestamp):
    return str(timestamp.strftime("%Y-%m-%d %H:%M"))


def get_current_price():
    current_price = db.reference(f"{db_root}/stockMarket/currentPrice").get()
    if current_price is None:
        return 0
    else:
        return int(current_price)


def set_current_price(new_price: int):
    db.reference(f"{db_root}/stockMarket/currentPrice").set(new_price)


def get_all_history():
    history = db.reference(f"{db_root}/stockMarket/history").get()
    if history is not None:
        return history
    else:
        return []


def get_history(since: datetime.timestamp):
    history = db.reference(f"{db_root}/stockMarket/history").order_by_key().start_at(timestamp_key(since)).get()
    if history is not None:
        return history
    else:
        return []


def append_to_history(value: int, timestamp: datetime.timestamp):
    db.reference(f"{db_root}/stockMarket/history").child(timestamp_key(timestamp)).set(value)


def get_user_portfolio(user: discord.User):
    portfolio = db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").get()

    if portfolio is None:
        db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").set(NEW_PORTFOLIO_DATA)
        return NEW_PORTFOLIO_DATA
    else:
        return portfolio


def buy_stock(user: discord.User, qty: int, price: int):
    current_time = datetime.now(timezone.utc)
    portfolio = get_user_portfolio(user)

    portfolio["stockQty"] = portfolio["stockQty"] + qty
    portfolio["totalDeposits"] = portfolio["totalDeposits"] + (qty * price)

    try:
        history = portfolio["history"]
    except KeyError:
        history = None

    if history is None:
        history = [{
            "timestamp": str(current_time),
            "action": BUY_ACTION,
            "qty": qty,
            "price": price
        }]
    else:
        history.append({
            "timestamp": str(current_time),
            "action": BUY_ACTION,
            "qty": qty,
            "price": price
        })

    portfolio["history"] = history

    db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").set(portfolio)


def sell_stock(user: discord.User, qty: int, price: int):
    current_time = datetime.now(timezone.utc)
    portfolio = get_user_portfolio(user)

    if qty > portfolio["stockQty"]:
        raise InsufficientStockError(user)

    portfolio["stockQty"] = portfolio["stockQty"] - qty
    portfolio["totalWithdrawals"] = portfolio["totalWithdrawals"] + (qty * price)

    try:
        history = portfolio["history"]
    except KeyError:
        history = None

    if history is None:
        history = [{
            "timestamp": str(current_time),
            "action": SELL_ACTION,
            "qty": qty,
            "price": price
        }]
    else:
        history.append({
            "timestamp": str(current_time),
            "action": SELL_ACTION,
            "qty": qty,
            "price": price
        })

    portfolio["history"] = history

    db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").set(portfolio)


NEW_PORTFOLIO_DATA = {
    "stockQty": 0,
    "history": [],
    "totalDeposits": 0,
    "totalWithdrawals": 0
}

BUY_ACTION = "buy"
SELL_ACTION = "sell"
REGISTER_ACTION = "register"
