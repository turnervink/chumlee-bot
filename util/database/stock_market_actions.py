from .config import db, db_root


def get_current_price():
    db.reference(f"{db_root}/stockMarket/currentPrice").get()


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
