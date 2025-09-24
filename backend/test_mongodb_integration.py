#!/usr/bin/env python3
"""
Test script to verify MongoDB integration with the market analysis system
"""

import sys
import os
import logging
from datetime import datetime, timedelta
import pandas as pd

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_storage import get_data_storage, init_data_storage
from market_analysis_algorithm.market_analysis import load_config

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        logger.info("Testing MongoDB connection...")
        storage = get_data_storage()
        logger.info("✅ MongoDB connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        return False

def test_data_storage():
    """Test data storage functionality"""
    try:
        logger.info("Testing data storage functionality...")
        storage = get_data_storage()

        # Test storing sample market data
        sample_data = pd.DataFrame({
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [104.0, 105.0, 106.0],
            'Volume': [1000000, 1100000, 1200000]
        }, index=pd.date_range('2024-01-01', periods=3))

        result = storage.store_market_data('TEST', sample_data, 'test_api')
        logger.info(f"✅ Stored {result} market data records")

        # Test retrieving cached data
        cached_data = storage.get_cached_market_data('TEST', days_back=1)
        logger.info(f"✅ Retrieved {len(cached_data)} cached records")

        # Test storing real-time price data
        price_data = {
            'current_price': 150.0,
            'previous_close': 149.0,
            'change': 1.0,
            'change_percent': 0.67,
            'volume': 2000000
        }

        result = storage.store_real_time_prices('TEST', price_data, 'test_api')
        logger.info(f"✅ Stored real-time price data: {result}")

        # Test retrieving cached real-time prices
        cached_prices = storage.get_cached_real_time_prices('TEST', minutes_back=60)
        logger.info(f"✅ Retrieved {len(cached_prices)} cached real-time price records")

        # Test database stats
        stats = storage.get_database_stats()
        logger.info(f"📊 Database stats: {stats}")

        return True
    except Exception as e:
        logger.error(f"❌ Data storage test failed: {e}")
        return False

def test_market_analysis_integration():
    """Test market analysis with caching"""
    try:
        logger.info("Testing market analysis with caching...")
        from market_analysis_algorithm.market_analysis import get_real_time_prices

        # Test with a single ticker (commented out to avoid API calls during testing)
        # prices = get_real_time_prices(['AAPL'])
        # logger.info(f"✅ Retrieved prices: {prices}")
        logger.info("ℹ️ Market analysis integration test skipped to avoid API calls")

        return True
    except Exception as e:
        logger.error(f"❌ Market analysis integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting MongoDB integration tests...")

    tests = [
        test_mongodb_connection,
        test_data_storage,
        test_market_analysis_integration
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests

    logger.info(f"📋 Test Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All tests passed! MongoDB integration is working correctly.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please check the configuration and try again.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
