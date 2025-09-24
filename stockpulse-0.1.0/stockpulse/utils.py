import time
import logging
import yaml
import os
import random
from functools import wraps

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

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

def load_config(config_path=None):
    """Load configuration from settings.yaml."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        if 'intra_day_interval' not in config['data']['yfinance']:
            config['data']['yfinance']['intra_day_interval'] = '1m'
            logger.warning("Missing 'intra_day_interval' in config, defaulting to '1m'")
        return config
    except FileNotFoundError:
        logger.warning("Config file not found, using default config")
        return {
            'data': {
                'yfinance': {
                    'tickers': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
                    'start_date': '2024-01-01',
                    'end_date': 'today',
                    'interval': '1d',
                    'intra_day_interval': '1m'
                }
            }
        }
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        raise
    
    
def setup_logging(log_dir=None, log_level=logging.INFO):
    """Set up logging for the package."""
    log_dir = log_dir or os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'stockpulse.log')),
            logging.StreamHandler()
        ]
    )