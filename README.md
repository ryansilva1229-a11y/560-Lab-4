# DSCI-560 Lab 4

**Team Members:** Elise Hadidi (1137648541), Jordan Davies (1857892197), Ryan Silva (6463166471) 
**Team Number:**  17


## Folder Structure

560-Lab-4/
├── Data/
│ ├── stocks.csv # Raw stock list scraped from NASDAQ
│ ├── arima_signals.csv # Output CSV with ARIMA signals
├── Scripts/
│ ├── arima.py # Script implementing ARIMA forecasting and signal generation
│ ├── webscraper2.py # Script to scrape NASDAQ stock data
│ ├── moving_average.py  # Script for Moving Average implementation
├── README.md 

## How to Run

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Install required packages:

pip install pandas numpy yfinance statsmodels scikit-learn selenium beautifulsoup4


### 2. Collect Stock Price Data
Run the web scraping script to collect the latest stock information:

python Scripts/data_collection.py

**What this script does:**
- Uses Selenium to navigate NASDAQ's stock screener
- Collects: Ticker symbol, Company name, Last sale price, Net change, % Change, Market cap
- Saves results to 'Data/stocks.csv'

### 3. Generate Moving Average Forecasts and Trading Signals
Run the Moving Average forecasting script:

python Scripts/[PUT SCRIPT NAME HERE JORDAN]

**What this script does:**

### 4. Generate ARIMA Forecasts and Trading Signals
Run the ARIMA forecasting script:

python Scripts/arima.py

**What this script does:**
- Loads the tickers from 'Data/stocks.csv'
- Downloads 1 year of historical prices using yfinance
- Trains ARIMA(5,1,0) model and forecasts next 5 days
- Calculates MAE and RMSE metrics
- Generates BUY/SELL/HOLD signals based on forecast vs. current price
- Saves results to 'Data/arima_signals.csv'

### 5. Mock Trading Environment



