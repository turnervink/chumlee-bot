from typing import List

import matplotlib.pyplot as plt
import numpy as np
import io
import discord

# TODO Adjust these based on some factors (what?) to simulate changing market conditions
MU = 0.0001  # Higher value = more bullish market
SIGMA = 0.01  # Higher value = more volatile market


def get_new_price(current_price: int):
    returns = [0]
    while returns[0] == 0:  # Prevent multiplying by 0, which would make the price 0 forever
        returns = np.random.normal(loc=MU, scale=SIGMA, size=1)

    return np.round(current_price*(1+returns).prod(), 0)


def graph_price_history(history: List[int]):
    # TODO Scale x axis label step based on number of values to make it more readable
    # TODO Generate more useful x axis labels, e.g. relative timestamps
    ax = plt.axes()
    ax.set_facecolor("black")

    x_values = list(reversed([i for i in range(1, len(history) + 1)]))

    plt.xticks(np.arange(min(x_values), max(x_values) + 1, step=1.0), labels=x_values)
    plt.plot(x_values, history, color="green")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    file = discord.File(buf, "plot.png")
    buf.close()
    plt.clf()
    return file


def simulate_prices(num_prices: int):
    current_price = 500
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

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    file = discord.File(buf, "plot.png")
    buf.close()
    return file

