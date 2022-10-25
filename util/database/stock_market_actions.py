import discord

from error.errors import InsufficientStockError
from .config import db, db_root


def get_current_price():
    current_price = db.reference(f"{db_root}/stockMarket/currentPrice").get()
    if current_price is None:
        return 0
    else:
        return int(current_price)


def set_current_price(new_price: int):
    db.reference(f"{db_root}/stockMarket/currentPrice").set(new_price)


def get_24h_history():
    history = db.reference(f"{db_root}/stockMarket/historyLast24Hours").get()
    if history is not None:
        return history
    else:
        return []


def get_7d_history():
    history = db.reference(f"{db_root}/stockMarket/historyLast7Days").get()
    if history is not None:
        return history
    else:
        return []


# TODO Store one history array with a max length, take slices for each window
def append_to_history(value: int):
    history_24h = get_24h_history()
    history_24h.append(value)
    while len(history_24h) > 24:
        history_24h.pop(0)
    db.reference(f"{db_root}/stockMarket/historyLast24Hours").set(history_24h)

    history_7d = get_7d_history()
    history_7d.append(value)
    while len(history_7d) > 168:
        history_7d.pop(0)
    db.reference(f"{db_root}/stockMarket/historyLast7Days").set(history_7d)


def get_user_portfolio(user: discord.User):
    # TODO New portfolio features
    # - Track buy/sell history
    # - Display return over time
    portfolio = db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").get()

    if portfolio is None:
        db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").set(NEW_PORTFOLIO_DATA)
        return NEW_PORTFOLIO_DATA
    else:
        return portfolio


def buy_stock(user: discord.User, qty: int):
    portfolio = get_user_portfolio(user)
    portfolio["stockQty"] = portfolio["stockQty"] + qty
    db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").set(portfolio)


def sell_stock(user: discord.User, qty: int):
    portfolio = get_user_portfolio(user)

    if qty > portfolio["stockQty"]:
        raise InsufficientStockError(user)

    portfolio["stockQty"] = portfolio["stockQty"] - qty

    db.reference(f"{db_root}/stockMarket/portfolios/{user.id}").set(portfolio)


NEW_PORTFOLIO_DATA = {
    "stockQty": 0,
    "history": []
}
