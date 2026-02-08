# Portfolio manager
import sys
import numpy as np
import sma_rsi

def main():
    if len(sys.argv) != 5:
        print("Usage: python main.py <tickers list> <window_size> <timeframe> <initial capital>")
        return
    
    tickers = sys.argv[1].split(",")
    window_size = int(sys.argv[2])
    timeframe = sys.argv[3]
    initial_capital = float(sys.argv[4])
    ongoing_capital = initial_capital

    tickers_dict = sma_rsi.calculate_indicators(tickers, window_size, timeframe)

    max_indices = len(tickers_dict[tickers[0]]) - 1

    portfolio_dict = {}
    for ticker in tickers:
        portfolio_dict[ticker] = 0

    portfolio_values = []

    for i in range(max_indices):
        for ticker in tickers:
            indication = tickers_dict[ticker].iloc[i]["Indication"]
            price = tickers_dict[ticker].iloc[i]["Price"]

            if indication == "Buy" and ongoing_capital >= price:
                print(f"Buying {ticker} at {price}")
                ongoing_capital -= price
                portfolio_dict[ticker] += 1

            elif indication == "Sell":
                if portfolio_dict[ticker] <= 0:
                    continue
                print(f"Selling {ticker} at {price}")
                for share in range(portfolio_dict[ticker]):
                    ongoing_capital += price
                portfolio_dict[ticker] = 0

        total_value = ongoing_capital
        for t in tickers:
            shares = portfolio_dict[t]
            price = tickers_dict[t].iloc[i]["Price"]
            total_value += shares * price

        portfolio_values.append(total_value)

    
    portfolio_values = np.array(portfolio_values)

    returns = np.diff(portfolio_values) / portfolio_values[:-1]

    rf_annual = 0.035
    rf_daily = rf_annual / 252

    excess_returns = returns - rf_daily

    if len(excess_returns) > 1 and np.std(excess_returns) != 0:
        sharpe_ratio = (np.mean(excess_returns) / np.std(excess_returns)) * np.sqrt(252)
    else:
        sharpe_ratio = 0

    print(f"Final capital: {ongoing_capital}")
    print(f"Annualized return: {(ongoing_capital / initial_capital) ** (365 / max_indices) - 1:.2%}")
    print(f"Sharpe ratio: {sharpe_ratio:.2f}")

if __name__ == "__main__":
    main()
    
