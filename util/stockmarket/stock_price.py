import numpy
import matplotlib.pyplot as plt

# https://ventsmagazine.com/2021/03/12/algorithm-used-for-weekly-turnips-price-calculator-in-animal-crossing-new-horizons/

# Each hour make a decision based on the trend of the last 24h
# Track the last 24h of prices in the database [57, 62, 89, 106, 82, 42...], append and shift as needed

BIG_INCREASE = 2
SMALL_INCREASE = 1
MINIMAL_CHANGE = 0
SMALL_DECREASE = -2
BIG_DECREASE = -2

CHANGE_RANGES = {
    BIG_INCREASE: (1.4, 2),
    SMALL_INCREASE: (1.2, 1.3),
    MINIMAL_CHANGE: (0.9, 1.1),
    SMALL_DECREASE: (0.7, 0.8),
    BIG_DECREASE: (0.3, 0.5)
}

# Big increase, Small Increase, Minimal Change, Small Decrease, Big Decrease
INCREASE_BOUND = [0, 0, 0.1, 0.2, 0.7]
STEEP_INCREASE = [0.01, 0.1, 0.4, 0.42, 0.07]
SLIGHT_INCREASE = [0.02, 0.23, 0.4, 0.3, 0.05]
FLAT_SLOPE = [0.03, 0.22, 0.5, 0.22, 0.03]
SLIGHT_DECREASE = [0.05, 0.3, 0.4, 0.23, 0.02]
STEEP_DECREASE = [0.07, 0.42, 0.4, 0.1, 0.01]
DECREASE_BOUND = [0.2, 0.7, 0.1, 0, 0]

SLOPE_RANGES = [
    (3, numpy.Inf, INCREASE_BOUND),
    (1, 3, STEEP_INCREASE),
    (0.1, 1, SLIGHT_INCREASE),
    (-0.1, 0.1, FLAT_SLOPE),
    (-0.1, 1, SLIGHT_DECREASE),
    (-1, -3, STEEP_DECREASE),
    (numpy.NINF, -3, DECREASE_BOUND)
]


def get_slope_range(s: int):
    for r in SLOPE_RANGES:
        if r[0] < s <= r[1]:
            return r[2]


FIRST_24_H = [500 for i in range(1, 25)]
HOURS = [i for i in range(1, 25)]

last_24_h = FIRST_24_H
for i in range(0, 72):
    current_value = last_24_h[len(last_24_h) - 2]

    slope, intercept = numpy.polyfit(range(0, 3), last_24_h[-3:], 1)
    slope_range = get_slope_range(slope)
    change_range = CHANGE_RANGES[numpy.random.choice([BIG_INCREASE, SMALL_INCREASE, MINIMAL_CHANGE, SMALL_DECREASE, BIG_DECREASE], p=slope_range)]

    new_value_multipler = numpy.round(numpy.random.uniform(change_range[0], change_range[1]), decimals=1)
    new_value = int(numpy.round(current_value * new_value_multipler, 0))

    last_24_h.pop(0)
    last_24_h.append(new_value)

print(last_24_h)

plt.plot(HOURS, last_24_h, marker='o')
plt.xticks(HOURS)
plt.show()
