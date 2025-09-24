
import time
import yfinance as yf
import pandas as pd
import logging
import os
from datetime import timedelta, datetime
import random
from .utils import rate_limit_decorator, load_config, BASE_DIR

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


@rate_limit_decorator(min_delay=5, max_delay=10, max_retries=3)
def fetch_single_ticker(ticker, start_date, end_date, interval):
    """
    Fetch data for a single ticker with rate limiting
    """
    logger.info(f"Fetching data for {ticker}")
    df = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    df.index.name = 'Date'
    return df

def fetch_stock_data_batch(tickers=None, start_date=None, end_date=None, interval='1d', save_to_csv=True, batch_size=3):
    config = load_config()
    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = tickers or config['data']['yfinance']['tickers']
    start_date = start_date or config['data']['yfinance']['start_date']
    end_date = end_date or config['data']['yfinance']['end_date']
    if end_date == 'today':
        end_date = datetime.now().strftime('%Y-%m-%d')
    logger.info(f"Fetching historical data for {len(tickers)} tickers from {start_date} to {end_date}")
    data = {}
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}: {batch}")
        try:
            batch_str = ' '.join(batch)
            batch_data = yf.download(batch_str, start=start_date, end=end_date, interval=interval)
            if not batch_data.empty:
                if len(batch) > 1 and batch_data.columns.nlevels > 1:
                    for ticker in batch:
                        try:
                            ticker_data = batch_data.xs(ticker, level=1, axis=1, drop_level=True)
                            ticker_data = ticker_data[['Open', 'High', 'Low', 'Close', 'Volume']]
                            ticker_data.index = pd.to_datetime(ticker_data.index)
                            ticker_data.index.name = 'Date'
                            data[ticker] = ticker_data
                            logger.info(f"Successfully fetched batch data for {ticker} ({len(ticker_data)} records)")
                            if save_to_csv:
                                save_stock_data_to_csv(ticker, ticker_data, data_type='historical')
                        except KeyError as e:
                            logger.warning(f"Error extracting batch data for {ticker}: {str(e)}")
                else:
                    ticker = batch[0]
                    ticker_data = batch_data[['Open', 'High', 'Low', 'Close', 'Volume']]
                    ticker_data.index = pd.to_datetime(ticker_data.index)
                    ticker_data.index.name = 'Date'
                    data[ticker] = ticker_data
                    logger.info(f"Successfully fetched batch data for {ticker} ({len(ticker_data)} records)")
                    if save_to_csv:
                        save_stock_data_to_csv(ticker, ticker_data, data_type='historical')
            time.sleep(random.uniform(3, 6))
        except Exception as e:
            logger.warning(f"Batch download failed for {batch}: {str(e)}")
            for ticker in batch:
                try:
                    stock_data = fetch_single_ticker(ticker, start_date, end_date, interval)
                    if not stock_data.empty:
                        stock_data.index = pd.to_datetime(stock_data.index)
                        stock_data.index.name = 'Date'
                        data[ticker] = stock_data
                        logger.info(f"Successfully fetched individual data for {ticker} ({len(stock_data)} records)")
                        if save_to_csv:
                            save_stock_data_to_csv(ticker, stock_data, data_type='historical')
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
    tickers = tickers or config['data']['yfinance']['tickers']
    interval = config['data']['yfinance'].get('intra_day_interval', '1m')
    logger.info(f"Fetching intraday data for {len(tickers)} tickers with period {period} and interval {interval}")
    data = {}
    for ticker in tickers:
        try:
            logger.info(f"Fetching intraday data for {ticker}")
            ticker_data = yf.download(ticker, period=period, interval=interval)
            if not ticker_data.empty:
                ticker_data = ticker_data[['Open', 'High', 'Low', 'Close', 'Volume']]
                ticker_data.index = pd.to_datetime(ticker_data.index)
                ticker_data.index.name = 'Date'
                data[ticker] = ticker_data
                logger.info(f"Successfully fetched intraday data for {ticker} ({len(ticker_data)} records)")
                if save_to_csv:
                    save_stock_data_to_csv(ticker, ticker_data, data_type='intraday')
            else:
                logger.warning(f"No intraday data found for {ticker}")
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
def fetch_single_intraday_ticker(ticker, period, interval):
    """
    Fetch intraday data for a single ticker with rate limiting
    """
    logger.info(f"Fetching intraday data for {ticker}")
    df = yf.download(ticker, period=period, interval=interval)
    df.index.name = 'Date'
    return df

@rate_limit_decorator(min_delay=5, max_delay=10, max_retries=3)
def fetch_single_intraday_data(tickers=None, period="1d", save_to_csv=True):
    """
    Fetch intraday stock data with enhanced rate limiting
    """
    config = load_config()
    if isinstance(tickers, str):
        tickers = [tickers]  # Convert single ticker to list
    tickers = tickers or config['data']['yfinance']['tickers']
    
    # Get the correct config key
    interval = config['data']['yfinance'].get('intra_day_interval', '1m')
    ticker_data = {}
    
    for ticker in tickers:
        try:
            stock_data = fetch_single_intraday_ticker(ticker, period, interval)
                
            if not stock_data.empty:
                stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
                ticker_data[ticker] = stock_data
                logger.info(f"Successfully fetched intraday data for {ticker} ({len(stock_data)} records)")
                
                # Save to CSV if requested
                if save_to_csv:
                    save_stock_data_to_csv(ticker, stock_data, data_type='intraday')
            else: 
                logger.warning(f"No intraday data found for {ticker}")
                
        except Exception as e:
            logger.error(f"Error fetching intraday data for {ticker}: {str(e)}")
            
        # Additional delay between intraday requests (they're more rate-limited)
        time.sleep(random.uniform(4, 8))
    
    return ticker_data

def save_stock_data_to_csv(ticker, data, data_type='historical'):
    """Save stock data to CSV at the specified location"""
    try:
        if data is None or data.empty:
            logger.error(f"No data to save for {ticker} ({data_type})")
            return
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in data.columns for col in required_cols):
            logger.error(f"Invalid columns in data for {ticker}: {data.columns.tolist()}")
            return
        # Ensure Date is a column
        data = data.reset_index()
        if 'Date' not in data.columns and data.index.name == 'Date':
            data['Date'] = data.index
        if 'Date' not in data.columns:
            logger.error(f"No Date column in data for {ticker}")
            return
        # Convert Date to string in correct format
        data['Date'] = pd.to_datetime(data['Date']).dt.strftime(
            '%Y-%m-%d' if data_type == 'historical' else '%Y-%m-%d %H:%M:%S'
        )
        logger.info(f"Saving {data_type} data for {ticker}:\n{data.head().to_string()}")
        output_dir = output_dir or os.path.join(os.getcwd(), 'data', 'raw', 'finance', data_type + '_data')
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{ticker}_{data_type}_{datetime.now().strftime('%Y%m%d')}.csv"
        file_path = os.path.join(output_dir, filename)
        data.to_csv(file_path, index=False)
        logger.info(f"Saved {data_type} data for {ticker} to {file_path}")
        latest_filename = f"{ticker}_latest_{data_type}.csv"
        latest_path = os.path.join(output_dir, latest_filename)
        data.to_csv(latest_path, index=False)
        logger.info(f"Saved latest {data_type} data for {ticker} to {latest_path}")
    except Exception as e:
        logger.error(f"Error saving data for {ticker}: {str(e)}")
        
        
def continuous_data_fetch(tickers=None, update_interval=60, data_type='intraday'):  # Increased to 2 minutes
    """
    Continuously fetch stock data every specified interval with enhanced rate limiting
    """
    config = load_config()
    if isinstance(tickers, str):
        tickers = [tickers]  # Convert single ticker to list
    tickers = tickers or config['data']['yfinance']['tickers']
    
    # Ensure minimum interval to avoid rate limiting
    if update_interval < 60:
        logger.warning(f"Update interval {update_interval}s is too short. Setting to 60s minimum.")
        update_interval = 60
    
    logger.info(f"Starting continuous data fetch for {tickers} every {update_interval} seconds")
    
    while True:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"Fetching data at {timestamp}")
            
            if data_type == 'intraday':
                data = intra_day_data(tickers=tickers, period="1d", save_to_csv=True)
            else:
                data = fetch_stock_data(tickers=tickers, save_to_csv=True)
            
            if data:
                logger.info(f"Successfully fetched data for {len(data)} tickers")
                yield data
            
            time.sleep(update_interval)
            
        except KeyboardInterrupt:
            logger.info("Continuous fetch stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in continuous fetch: {str(e)}")
            # Wait longer on error
            time.sleep(min(update_interval * 2, 600))  # Max 10 minutes

@rate_limit_decorator(min_delay=1, max_delay=3, max_retries=2)
def get_single_ticker_info(ticker):
    """
    Get info for a single ticker with rate limiting
    """
    stock = yf.Ticker(ticker)
    return stock.info

def get_real_time_prices(tickers=None):
    """
    Get real-time stock prices with enhanced rate limiting
    """
    config = load_config()
    if isinstance(tickers, str):
        tickers = [tickers]  # Convert single ticker to list
    tickers = tickers or config['data']['yfinance']['tickers']
    
    prices = {}
    for ticker in tickers:
        try:
            info = get_single_ticker_info(ticker)
            
            prices[ticker] = {
                'symbol': ticker,
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'change': info.get('currentPrice', 0) - info.get('previousClose', 0),
                'change_percent': ((info.get('currentPrice', 0) - info.get('previousClose', 0)) / info.get('previousClose', 1)) * 100,
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'timestamp': datetime.now().isoformat()
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
        
        # Small delay between price requests
        time.sleep(random.uniform(0.5, 1.5))
    
    return prices

def get_latest_data(ticker, data_type='historical'):
    """
    Get the latest saved data for a ticker
    """
    try:
        if data_type == 'intraday':
            csv_dir = os.path.join(BASE_DIR, 'data', 'raw', 'finance', 'intraday_data')
        else:
            csv_dir = os.path.join(BASE_DIR, 'data', 'raw', 'finance', 'historical_data')
        
        latest_filename = f"{ticker}_latest_{data_type}.csv"
        latest_path = os.path.join(csv_dir, latest_filename)
        
        if os.path.exists(latest_path):
            data = pd.read_csv(latest_path, index_col='Date', parse_dates=['Date'])
            return data
        else:
            logger.warning(f"No latest {data_type} data found for {ticker}")
            return None
            
    except Exception as e:
        logger.error(f"Error loading latest data for {ticker}: {str(e)}")
        return None

