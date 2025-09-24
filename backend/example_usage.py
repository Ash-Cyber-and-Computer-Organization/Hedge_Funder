#!/usr/bin/env python3
"""
Example usage of the Hedge Funder Backend with MongoDB integration
"""

import sys
import os
import logging
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def example_real_time_prices():
    """Example: Get real-time stock prices with caching"""
    logger.info("📈 Example 1: Fetching real-time prices...")

    try:
        from market_analysis_algorithm.market_analysis import get_real_time_prices

        # Fetch real-time prices for popular stocks
        tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
        prices = get_real_time_prices(tickers)

        logger.info("Real-time prices:")
        for ticker, data in prices.items():
            if 'cached' in data and data['cached']:
                logger.info(f"  {ticker}: ${data['current_price']:.2f} (cached)")
            else:
                logger.info(f"  {ticker}: ${data['current_price']:.2f} (live)")

        return prices

    except Exception as e:
        logger.error(f"❌ Error fetching real-time prices: {e}")
        return {}

def example_historical_data():
    """Example: Get historical data with caching"""
    logger.info("\n📊 Example 2: Fetching historical data...")

    try:
        from market_analysis_algorithm.market_analysis import fetch_stock_data_batch

        # Fetch historical data for the past month
        tickers = ['AAPL', 'GOOGL']
        data = fetch_stock_data_batch(
            tickers=tickers,
            start_date='2024-01-01',
            end_date='2024-01-31'
        )

        logger.info("Historical data summary:")
        for ticker, df in data.items():
            logger.info(f"  {ticker}: {len(df)} records from {df.index.min()} to {df.index.max()}")

        return data

    except Exception as e:
        logger.error(f"❌ Error fetching historical data: {e}")
        return {}

def example_intraday_data():
    """Example: Get intraday data with caching"""
    logger.info("\n⏰ Example 3: Fetching intraday data...")

    try:
        from market_analysis_algorithm.market_analysis import intra_day_data

        # Fetch intraday data for today
        tickers = ['AAPL']
        data = intra_day_data(tickers=tickers, period="1d")

        logger.info("Intraday data summary:")
        for ticker, df in data.items():
            logger.info(f"  {ticker}: {len(df)} records")

        return data

    except Exception as e:
        logger.error(f"❌ Error fetching intraday data: {e}")
        return {}

def example_technical_analysis():
    """Example: Perform technical analysis"""
    logger.info("\n📈 Example 4: Running technical analysis...")

    try:
        from market_analysis_algorithm.market_analysis import run_market_analysis

        # Run analysis for a few tickers
        result = run_market_analysis(['AAPL', 'GOOGL'])

        logger.info("Analysis results:")
        for ticker, analysis in result['analysis'].items():
            logger.info(f"  {ticker}: {analysis['action']} - {analysis['reason']}")

        return result

    except Exception as e:
        logger.error(f"❌ Error running technical analysis: {e}")
        return {}

def example_data_storage():
    """Example: Direct data storage operations"""
    logger.info("\n💾 Example 5: Direct data storage operations...")

    try:
        from data_storage import get_data_storage
        import pandas as pd

        storage = get_data_storage()

        # Get database statistics
        stats = storage.get_database_stats()
        logger.info(f"Database stats: {stats}")

        # Store sample data
        sample_data = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [105.0, 106.0],
            'Low': [99.0, 100.0],
            'Close': [104.0, 105.0],
            'Volume': [1000000, 1100000]
        }, index=pd.date_range('2024-01-01', periods=2))

        stored = storage.store_market_data('EXAMPLE', sample_data, 'demo')
        logger.info(f"Stored {stored} records for EXAMPLE ticker")

        # Retrieve cached data
        cached = storage.get_cached_market_data('EXAMPLE', days_back=1)
        logger.info(f"Retrieved {len(cached)} cached records")

        return stats

    except Exception as e:
        logger.error(f"❌ Error with data storage: {e}")
        return {}

def main():
    """Run all examples"""
    logger.info("🚀 Hedge Funder Backend - Usage Examples")
    logger.info("=" * 50)

    examples = [
        example_real_time_prices,
        example_historical_data,
        example_intraday_data,
        example_technical_analysis,
        example_data_storage
    ]

    results = {}

    for example in examples:
        try:
            result = example()
            results[example.__name__] = result
        except Exception as e:
            logger.error(f"❌ Example {example.__name__} failed: {e}")

    logger.info("\n" + "=" * 50)
    logger.info("📋 Summary of Results:")
    for name, result in results.items():
        if result:
            logger.info(f"✅ {name}: Success")
        else:
            logger.info(f"❌ {name}: Failed or empty")

    logger.info("\n💡 Tips:")
    logger.info("- First run may take longer due to caching")
    logger.info("- Subsequent runs will use cached data for better performance")
    logger.info("- Check logs for detailed information about API calls and caching")
    logger.info("- Update .env file with your actual API keys for full functionality")

if __name__ == "__main__":
    main()
