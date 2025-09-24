# StockPulse
A robust Python package for fetching and managing stock market data with rate-limiting.

## Installation
```bash
pip install stockpulse
```

## Usage
```
from stockpulse import fetch_stock_data, intra_day_data, get_real_time_prices

# Fetch historical data
data = fetch_stock_data(tickers=["AAPL", "TSLA"], save_to_csv=True)

# Fetch intraday data
intraday = intra_day_data(tickers=["AAPL"], period="1d")

# Get real-time prices
prices = get_real_time_prices(tickers=["AAPL", "GOOGL"])
print(prices)

```

## Features

- Fetch historical and intraday stock data using yfinance.
- Rate-limiting to avoid API restrictions.
- Save data to CSV with organized file structure.
- Continuous data fetching for real-time applications.
