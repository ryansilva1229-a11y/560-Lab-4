# Portfolio manager
import sys
import sma_rsi

def main():
    if len(sys.argv) != 5:
        print("Usage: python main.py <tickers list> <window_size> <timeframe> <initial capital>")
        return
    
    tickers = sys.argv[1].split(",")
    window_size = int(sys.argv[2])
    timeframe = sys.argv[3]
    initial_capital = float(sys.argv[4])

    tickers_dict = sma_rsi.calculate_indicators(tickers, window_size, timeframe)

    max_indices = len(tickers_dict[tickers[0]]) - 1

    portfolio_dict = {}
    for ticker in tickers:
        portfolio_dict[ticker] = 0

    for i in range(max_indices):
        for ticker in tickers:
            indication = tickers_dict[ticker].iloc[i]["Indication"]
            price = tickers_dict[ticker].iloc[i]["Price"]

            if indication == "Buy" and initial_capital >= price:
                print(f"Buying {ticker} at {price}")
                initial_capital -= price
                portfolio_dict[ticker] += 1

            elif indication == "Sell":
                if portfolio_dict[ticker] <= 0:
                    continue
                print(f"Selling {ticker} at {price}")
                for share in range(portfolio_dict[ticker]):
                    initial_capital += price
                portfolio_dict[ticker] = 0

    print(f"Final capital: {initial_capital}")

if __name__ == "__main__":
    main()
    
