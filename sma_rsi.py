import yfinance
import pandas as pd
import moving_avg
import rsi

def process_ticker(ticker, window_size, timeframe):
    data = yfinance.download(ticker, period=timeframe)
    prices = data["Close"]

    sma_df = moving_avg.calc_simple_moving_avg(prices, window_size)

    price_values = []
    for price in prices.values:
        price_values.append(price[0])

    rsi_values = []
    index = 0
    for price in prices.values:
        price_values_short = price_values[:index + 1]
        rsi_value = rsi.calculate_rsi(price_values_short, window_size)
        rsi_values.append(rsi_value)
        index += 1

    ticker_df = pd.DataFrame({
        "Date": sma_df["Date"],
        "Price": sma_df["Price"],
        "SMA": sma_df["SMA"],
        "RSI": rsi_values
    })

    ticker_df["SMA_smooth"] = ticker_df["SMA"].rolling(5).mean()
    ticker_df["SMA_slope"] = ticker_df["SMA_smooth"].diff()

    return ticker_df

def calculate_indicators(tickers, window_size, timeframe):
    tickers_dict = {}
    for ticker in tickers:

        ticker_df = process_ticker(ticker, window_size, timeframe)

        indication = []

        for i in range(len(ticker_df)):
            rsi = ticker_df["RSI"].iloc[i]
            sma_slope = ticker_df["SMA_slope"].iloc[i]

            action = "No action"

            if i > 0 and rsi is not None and pd.notna(sma_slope):

                if sma_slope > 0:
                    if 40 <= rsi <= 50:
                        action = "Buy"

                elif sma_slope < 0:
                    if 50 <= rsi <= 60:
                        action = "Sell"

                else:
                    if rsi < 30:
                        action = "Buy"
                    elif rsi > 70:
                        action = "Sell"

            indication.append(action)

        ticker_df["Indication"] = indication

        tickers_dict[ticker] = ticker_df

    return tickers_dict
    