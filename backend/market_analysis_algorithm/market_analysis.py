import time
import requests
import pandas as pd
import logging
import os
import sys
from datetime import timedelta, datetime
import random
import numpy as np
from functools import wraps

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set default MongoDB connection if not set
if not os.environ.get('MONGODB_URL'):
    os.environ['MONGODB_URL'] = 'mongodb+srv://dada4ash_db_user:Jack247x@cluster0.j8emjgs.mongodb.net/'
if not os.environ.get('MONGODB_DATABASE'):
    os.environ['MONGODB_DATABASE'] = 'hedge_funder'

from data_storage import get_data_storage

logger = logging.getLogger(__name__)

# Rate limiting decorator from stockpulse
def rate_limit_decorator(min_delay=5, max_delay=10, max_retries=3):
    """Decorator to add rate limiting and retry logic to functions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    delay = random.uniform(min_delay, max_delay)
                    if attempt > 0:
                        logger.info(f"Retrying in {delay:.2f} seconds (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    return func(*args, **kwargs)
                except Exception as e:
                    error_msg = str(e).lower()
                    if 'rate limit' in error_msg or 'too many requests' in error_msg:
                        if attempt < max_retries - 1:
                            backoff_time = (2 ** attempt) * 60 + random.uniform(0, 30)
                            logger.warning(f"Rate limit hit. Waiting {backoff_time:.1f} seconds before retry...")
                            time.sleep(backoff_time)
                            continue
                        else:
                            logger.error(f"Rate limit exceeded after {max_retries} attempts")
                            raise
                    else:
                        raise
            return None
        return wrapper
    return decorator

# Load config (simplified)
def load_config():
    return {
        'data': {
            'tickers': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
            'start_date': '2024-01-01',
            'end_date': 'today',
            'interval': '1d',
            'intra_day_interval': '1m'
        },
        'api_keys': {
            'finnhub': os.environ.get('FINNHUB_API_KEY', 'd301361r01qm5loaat7gd301361r01qm5loaat80'),
            'alpha_vantage': os.environ.get('ALPHA_VANTAGE_API_KEY', '18PFVTQ6H4MR6SI2'),
            'twelve_data': os.environ.get('TWELVE_DATA_API_KEY', '38b79e226bac465fbaee065d90c1683f')
        }
    }

@rate_limit_decorator(min_delay=5, max_delay=10, max_retries=3)
def fetch_single_ticker(ticker, start_date, end_date, interval):
    """
    Fetch data for a single ticker with rate limiting using Alpha Vantage
    """
    config = load_config()
    api_key = config['api_keys']['alpha_vantage']
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}&outputsize=full"
    logger.info(f"Fetching data for {ticker} from Alpha Vantage")
    response = requests.get(url)
    data = response.json()
    if 'Time Series (Daily)' in data:
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.astype(float)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df.index.name = 'Date'
        return df
    else:
        logger.error(f"Error fetching data for {ticker}: {data}")
        return pd.DataFrame()

def fetch_stock_data_batch(tickers=None, start_date=None, end_date=None, interval='1d', save_to_csv=True, batch_size=3):
    config = load_config()
    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = tickers or config['data']['tickers']
    start_date = start_date or config['data']['start_date']
    end_date = end_date or config['data']['end_date']
    if end_date == 'today':
        end_date = datetime.now().strftime('%Y-%m-%d')

    logger.info(f"Fetching historical data for {len(tickers)} tickers from {start_date} to {end_date}")

    # Initialize data storage
    storage = get_data_storage()
    data = {}

    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}: {batch}")

        try:
            for ticker in batch:
                try:
                    # Check for cached data first
                    cached_data = storage.get_cached_market_data(ticker, days_back=30)
                    if cached_data:
                        # Convert cached data back to DataFrame
                        df = pd.DataFrame(cached_data)
                        df['date'] = pd.to_datetime(df['date'])
                        df.set_index('date', inplace=True)
                        df = df[['open', 'high', 'low', 'close', 'volume']]
                        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                        data[ticker] = df
                        logger.info(f"Using cached data for {ticker} ({len(df)} records)")
                        continue

                    # Fetch fresh data if not cached
                    ticker_data = fetch_single_ticker(ticker, start_date, end_date, interval)
                    if not ticker_data.empty:
                        ticker_data = ticker_data[['Open', 'High', 'Low', 'Close', 'Volume']]
                        ticker_data.index = pd.to_datetime(ticker_data.index)
                        ticker_data.index.name = 'Date'
                        data[ticker] = ticker_data

                        # Store in MongoDB
                        storage.store_market_data(ticker, ticker_data, 'alpha_vantage')

                        logger.info(f"Successfully fetched and cached data for {ticker} ({len(ticker_data)} records)")
                    else:
                        logger.warning(f"No data found for {ticker}")
                except Exception as e:
                    logger.error(f"Error fetching individual data for {ticker}: {str(e)}")
                time.sleep(random.uniform(2, 4))
        except Exception as e:
            logger.warning(f"Batch download failed for {batch}: {str(e)}")
            for ticker in batch:
                try:
                    stock_data = fetch_single_ticker(ticker, start_date, end_date, interval)
                    if not stock_data.empty:
                        stock_data.index = pd.to_datetime(stock_data.index)
                        stock_data.index.name = 'Date'
                        data[ticker] = stock_data

                        # Store in MongoDB
                        storage.store_market_data(ticker, stock_data, 'alpha_vantage')

                        logger.info(f"Successfully fetched individual data for {ticker} ({len(stock_data)} records)")
                    else:
                        logger.warning(f"No data found for {ticker}")
                except Exception as e:
                    logger.error(f"Error fetching individual data for {ticker}: {str(e)}")
                time.sleep(random.uniform(2, 4))
    return data

def intra_day_data(tickers=None, period="1d", save_to_csv=True):
    config = load_config()
    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = tickers or config['data']['tickers']
    interval = config['data'].get('intra_day_interval', '1m')
    api_key = config['api_keys']['twelve_data']

    logger.info(f"Fetching intraday data for {len(tickers)} tickers with period {period} and interval {interval}")

    # Initialize data storage
    storage = get_data_storage()
    data = {}

    for ticker in tickers:
        try:
            # Check for cached data first
            cached_data = storage.get_cached_intraday_data(ticker, hours_back=24)
            if cached_data:
                # Convert cached data back to DataFrame
                df = pd.DataFrame(cached_data)
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                df = df[['open', 'high', 'low', 'close', 'volume']]
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                data[ticker] = df
                logger.info(f"Using cached intraday data for {ticker} ({len(df)} records)")
                continue

            # Fetch fresh data if not cached
            logger.info(f"Fetching intraday data for {ticker} from Twelve Data")
            url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval={interval}&outputsize=500&apikey={api_key}"
            response = requests.get(url)
            data_response = response.json()

            if 'values' in data_response:
                df = pd.DataFrame(data_response['values'])
                df = df.astype(float)
                df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
                df.index = pd.to_datetime(df['Date'])
                df.index.name = 'Date'
                df = df.sort_index()
                data[ticker] = df

                # Store in MongoDB
                storage.store_intraday_data(ticker, df, 'twelve_data')

                logger.info(f"Successfully fetched and cached intraday data for {ticker} ({len(df)} records)")
            else:
                logger.warning(f"No intraday data found for {ticker}: {data_response}")
            time.sleep(random.uniform(4, 8))
        except Exception as e:
            logger.error(f"Error fetching intraday data for {ticker}: {str(e)}")
    return data

def fetch_stock_data(tickers=None, start_date=None, end_date=None, interval='1d', save_to_csv=False):
    """
    Original function with enhanced rate limiting
    """
    return fetch_stock_data_batch(tickers, start_date, end_date, interval, save_to_csv)

@rate_limit_decorator(min_delay=5, max_delay=10, max_retries=3)
def get_real_time_prices(tickers=None):
    """
    Get real-time stock prices with enhanced rate limiting using Finnhub
    """
    config = load_config()
    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = tickers or config['data']['tickers']
    api_key = config['api_keys']['finnhub']

    # Initialize data storage
    storage = get_data_storage()
    prices = {}

    for ticker in tickers:
        try:
            # Check for cached data first
            cached_data = storage.get_cached_real_time_prices(ticker, minutes_back=60)
            if cached_data:
                # Use the most recent cached data
                latest_data = cached_data[0]
                prices[ticker] = {
                    'symbol': ticker,
                    'current_price': latest_data.get('current_price', 0),
                    'previous_close': latest_data.get('previous_close', 0),
                    'change': latest_data.get('change', 0),
                    'change_percent': latest_data.get('change_percent', 0),
                    'volume': latest_data.get('volume', 0),
                    'market_cap': 0,
                    'timestamp': latest_data.get('timestamp', datetime.now().isoformat()),
                    'cached': True
                }
                logger.info(f"Using cached real-time price for {ticker}")
                continue

            # Fetch fresh data if not cached
            url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
            response = requests.get(url)
            data = response.json()

            if 'c' in data:
                price_data = {
                    'symbol': ticker,
                    'current_price': data.get('c', 0),
                    'previous_close': data.get('pc', 0),
                    'change': data.get('c', 0) - data.get('pc', 0),
                    'change_percent': ((data.get('c', 0) - data.get('pc', 0)) / data.get('pc', 1)) * 100 if data.get('pc', 0) != 0 else 0,
                    'volume': data.get('v', 0),
                    'market_cap': 0,  # Finnhub doesn't provide market cap in quote endpoint
                    'timestamp': datetime.now().isoformat()
                }
                prices[ticker] = price_data

                # Store in MongoDB
                storage.store_real_time_prices(ticker, price_data, 'finnhub')

                logger.info(f"Successfully fetched and cached real-time price for {ticker}")
            else:
                logger.error(f"Error fetching real-time price for {ticker}: {data}")
                prices[ticker] = {
                    'symbol': ticker,
                    'current_price': 0,
                    'previous_close': 0,
                    'change': 0,
                    'change_percent': 0,
                    'volume': 0,
                    'market_cap': 0,
                    'timestamp': datetime.now().isoformat(),
                    'error': data
                }
        except Exception as e:
            logger.error(f"Error fetching real-time price for {ticker}: {str(e)}")
            prices[ticker] = {
                'symbol': ticker,
                'current_price': 0,
                'previous_close': 0,
                'change': 0,
                'change_percent': 0,
                'volume': 0,
                'market_cap': 0,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }

        time.sleep(random.uniform(0.5, 1.5))

    return prices

# New analysis functions
def calculate_sma(data, window=20):
    """Calculate Simple Moving Average"""
    return data['Close'].rolling(window=window).mean()

def calculate_ema(data, window=20):
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=window).mean()

def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze_stock(data, ticker):
    """Analyze stock data and suggest trade action"""
    if data.empty:
        return {'action': 'hold', 'reason': 'No data available'}
    
    # Calculate indicators
    data['SMA_20'] = calculate_sma(data, 20)
    data['EMA_20'] = calculate_ema(data, 20)
    data['RSI'] = calculate_rsi(data, 14)
    
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    # Simple strategy: Buy if price above SMA and RSI < 70, Sell if below SMA and RSI > 30
    if latest['Close'] > latest['SMA_20'] and latest['RSI'] < 70:
        action = 'buy'
        reason = f"Price ({latest['Close']:.2f}) above SMA ({latest['SMA_20']:.2f}) and RSI ({latest['RSI']:.2f}) indicates potential upside"
    elif latest['Close'] < latest['SMA_20'] and latest['RSI'] > 30:
        action = 'sell'
        reason = f"Price ({latest['Close']:.2f}) below SMA ({latest['SMA_20']:.2f}) and RSI ({latest['RSI']:.2f}) indicates potential downside"
    else:
        action = 'hold'
        reason = f"Price ({latest['Close']:.2f}) relative to SMA ({latest['SMA_20']:.2f}) and RSI ({latest['RSI']:.2f}) suggests holding"
    
    return {
        'ticker': ticker,
        'action': action,
        'reason': reason,
        'current_price': latest['Close'],
        'sma_20': latest['SMA_20'],
        'rsi': latest['RSI']
    }

def place_trade(action, ticker, quantity=1, price=None):
    """Simple trade placement simulation"""
    logger.info(f"Placing {action} order for {quantity} shares of {ticker} at price {price}")
    # In a real implementation, integrate with a trading API like Alpaca
    return {'status': 'success', 'message': f'{action} order placed for {ticker}'}

def run_market_analysis(tickers=None):
    """Main function to run market analysis and place trades"""
    logger.info("Starting market analysis")

    # Initialize data storage
    storage = get_data_storage()

    # Fetch real-time data
    prices = get_real_time_prices(tickers)

    # Fetch historical data for analysis
    historical_data = fetch_stock_data(tickers, interval='1d')

    analysis_results = {}
    for ticker, data in historical_data.items():
        analysis = analyze_stock(data, ticker)
        analysis_results[ticker] = analysis
        logger.info(f"Analysis for {ticker}: {analysis}")

        # Store trade signal in MongoDB as JSON
        storage.store_trade_signal(
            ticker=analysis['ticker'],
            action=analysis['action'],
            reason=analysis['reason'],
            current_price=analysis['current_price'],
            sma_20=analysis['sma_20'],
            rsi=analysis['rsi']
        )

        if analysis['action'] != 'hold':
            trade_result = place_trade(analysis['action'], ticker)
            # Store transaction in MongoDB as JSON
            storage.store_transaction(
                user_id='default',
                ticker=ticker,
                action=analysis['action'],
                quantity=1,
                price=analysis['current_price'],
                total_value=analysis['current_price']
            )

    return {'prices': prices, 'analysis': analysis_results}

# Added function to setup logging
def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    setup_logging()
    result = run_market_analysis()
    print(result)