import sys
import numpy as np
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

def arima_forecast(prices, order=(5, 1, 0), steps=1):
    if len(prices) < 10:
        return None
    model = ARIMA(prices, order=order)
    model_fit = model.fit()
    return model_fit.forecast(steps=steps)

def generate_signal(current_price, forecast_price, threshold=0.05):
    if forecast_price > current_price * (1 + threshold):
        return "Buy"
    elif forecast_price < current_price * (1 - threshold):
        return "Sell"
    else:
        return "Hold"

def main():
    if len(sys.argv) != 5:
        print("Usage: python main.py <tickers list> <forecast steps> <timeframe> <initial capital>")
        return

    tickers = sys.argv[1].split(",")
    forecast_steps = int(sys.argv[2])
    timeframe = sys.argv[3]
    initial_capital = float(sys.argv[4])
    ongoing_capital = initial_capital

    portfolio_dict = {ticker: 0 for ticker in tickers}
    portfolio_values = []

    tickers_data = {}
    for ticker in tickers:
        hist = yf.download(ticker, period=timeframe, progress=False)
        if hist.empty or len(hist) < forecast_steps + 10:
            continue
        tickers_data[ticker] = hist["Close"].reset_index(drop=True)
    if not tickers_data:
        return

    max_len = min(len(prices) for prices in tickers_data.values())

    for i in range(forecast_steps, max_len):
        for ticker, prices in tickers_data.items():
            window_prices = prices[:i]
            forecast = arima_forecast(window_prices, steps=forecast_steps)
            if forecast is None:
                continue

            current_price = float(prices.iloc[i])
            forecast_mean = float(forecast.mean())
            signal = generate_signal(current_price, forecast_mean)

            if signal == "Buy" and ongoing_capital >= current_price:
                print(f"Buying {ticker} at {current_price:.2f}")
                ongoing_capital -= current_price
                portfolio_dict[ticker] += 1

            elif signal == "Sell" and portfolio_dict[ticker] > 0:
                print(f"Selling {ticker} at {current_price:.2f}")
                ongoing_capital += portfolio_dict[ticker] * current_price
                portfolio_dict[ticker] = 0

        total_value = ongoing_capital + sum(portfolio_dict[t] * tickers_data[t].iloc[i] for t in tickers_data)
        portfolio_values.append(float(total_value))

    if len(portfolio_values) < 2:
        return

    returns = np.diff(portfolio_values) / portfolio_values[:-1]
    rf_daily = 0.035 / 252
    excess_returns = returns - rf_daily
    sharpe_ratio = (np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)) if np.std(excess_returns) != 0 else 0
    annualized_return = ((portfolio_values[-1] / initial_capital) ** (252 / len(portfolio_values))) - 1

    print(f"\nFinal capital: {ongoing_capital:.2f}")
    print(f"Annualized return: {annualized_return:.2%}")
    print(f"Sharpe ratio: {sharpe_ratio:.2f}")

if __name__ == "__main__":
    main()
