import matplotlib.pyplot as plt
import numpy as np

from util.database import stock_market_actions

MU = 0.0001
SIGMA = 0.01


def get_last_24h():
    last_24_h = stock_market_actions.get_24h_history()
    print(last_24_h)


def plot_prices():
    current_price = 500
    prices = []

    for i in range(0, 24):
        returns = np.random.normal(loc=MU, scale=SIGMA, size=1)
        current_price = current_price*(1+returns).prod()

        prices.append(current_price)
        if len(prices) > 24:
            prices.pop(0)

    ax = plt.axes()
    ax.set_facecolor("black")
    plt.plot([i for i in range(0, len(prices))], prices, color="green")
    plt.xticks([i for i in range(1, len(prices) + 1)])

    plt.show()

get_last_24h()
