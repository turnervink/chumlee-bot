import numpy as np
import matplotlib.pyplot as plt

mu = 0.0001
sigma = 0.01
start_price = 500

current_price = start_price
prices = []
for i in range(0, 24):
    returns = np.random.normal(loc=mu, scale=sigma, size=1)
    current_price = current_price*(1+returns).prod()

    prices.append(current_price)
    if len(prices) > 24:
        prices.pop(0)

ax = plt.axes()
ax.set_facecolor("black")
plt.plot([i for i in range(0, len(prices))], prices, color="green")
plt.xticks([i for i in range(1, len(prices) + 1)])

plt.show()
