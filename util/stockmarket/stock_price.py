from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import io
import discord

# TODO Adjust these based on some factors (what?) to simulate changing market conditions
MU = 0.0002  # Higher value = more bullish market
SIGMA = 0.01  # Higher value = more volatile market


def get_new_price(current_price: int):
    returns = [0]
    while returns[0] == 0:  # Prevent multiplying by 0, which would make the price 0 forever
        returns = np.random.normal(loc=MU, scale=SIGMA, size=1)

    return np.round(current_price*(1+returns).prod(), 0)


def calculate_price_change_pct(old_price: int, new_price: int):
    return np.round((new_price - old_price)/old_price*100, 2)


def calculate_portfolio_return(old_price: int, new_price: int, shares: int):
    return np.round(((new_price - old_price)*shares)/old_price*100, 2)


def graph_price_history(history: List[Tuple[str, int]]):
    timestamps = list(map(lambda x: str(datetime.strptime(x[0], "%Y-%m-%d %H:%M").strftime("%H:%M")), history))
    prices = list(map(lambda x: x[1], history))
    step = int(np.ceil(len(history)/12))

    change_pct = calculate_price_change_pct(prices[0], prices[-1])
    graph_colour = "green" if change_pct >= 0 else "red"

    ax = plt.axes()
    ax.set_facecolor("black")

    plt.xticks(np.arange(0, len(timestamps), step))
    plt.plot(timestamps, list(prices), color=graph_colour)
    plt.fill_between(timestamps, list(prices), min(list(prices)) - 5, color=graph_colour)

    ax.set_xticklabels(timestamps[::step], rotation=45)
    ax.set_xlim(0, len(timestamps)-1)
    ax.set_ylim(min(prices) - 5, max(prices) + 5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    file = discord.File(buf, "plot.png")
    buf.close()
    plt.clf()
    return file


def simulate_prices(num_prices: int):
    current_price = 100
    prices = []

    for i in range(0, num_prices):
        returns = [0]
        while returns[0] == 0:  # Prevent multiplying by 0, which would make the price 0 forever
            returns = np.random.normal(loc=MU, scale=SIGMA, size=1)

        current_price = np.round(current_price*(1+returns).prod(), 0)

        prices.append(current_price)

    ax = plt.axes()
    ax.set_facecolor("black")
    plt.plot([i for i in range(0, num_prices)], prices, color="green")
    plt.xticks([i for i in range(1, num_prices + 1)])

    plt.show()


if __name__ == "__main__":
    simulate_prices(8760)
