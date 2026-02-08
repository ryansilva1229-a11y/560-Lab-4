import os
import pandas as pd
import yfinance as yf
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

csv_path = os.path.join("..", "Data", "stocks.csv")
df = pd.read_csv(csv_path)

tickers = df["Ticker"].head(50).tolist()

def arima_forecast(prices, order=(5, 1, 0), steps=5):
    model = ARIMA(prices, order=order)
    model_fit = model.fit()
    return model_fit.forecast(steps=steps)

def generate_signal(current_price, forecast_mean):
    current_price = float(np.squeeze(current_price))
    forecast_mean = float(np.squeeze(forecast_mean))

    if forecast_mean > current_price:
        return "BUY"
    elif forecast_mean < current_price:
        return "SELL"
    else:
        return "HOLD"

results = []

for ticker in tickers:

    hist = yf.download(ticker, period="1y", progress=False)

    if hist.empty or len(hist) < 60:
        continue

    prices = hist["Close"]

    train = prices[:-5]
    test = prices[-5:]

    forecast = arima_forecast(train, steps=5)

    mae = mean_absolute_error(test, forecast)
    rmse = np.sqrt(mean_squared_error(test, forecast))

    signal = generate_signal(prices.iloc[-1], forecast.mean())

    results.append({
        "Ticker": ticker,
        "Signal": signal
    })

output_path = os.path.join("..", "Data", "arima_signals.csv")
results_df = pd.DataFrame(results)
results_df.to_csv(output_path, index=False)
