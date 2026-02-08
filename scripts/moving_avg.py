# This script is used in sma_rsi.py to compute the simple moving average

import pandas as pd

# Calculate the simple moving average for a given series of prices and a specified window size
# Return a DataFrame with the original prices and the calculated moving average
def calc_simple_moving_avg(prices_series, window):
    dates = prices_series.index
    prices = []
    for price in prices_series.values:
        prices.append(price[0])
    curr_prices = []
    moving_avgs = []
    for i in range(len(prices)):
        if len(curr_prices) < window:
            curr_prices.append(prices[i])
        else:
            curr_prices.pop(0)
            curr_prices.append(prices[i])

        avg = sum(curr_prices) / len(curr_prices)
        moving_avgs.append(avg)

    return pd.DataFrame({"Date": dates, "Price": prices, "SMA": moving_avgs})
