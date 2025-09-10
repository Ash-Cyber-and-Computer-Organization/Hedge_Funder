#!/usr/bin/env python3
"""
Test script for the News-Based Trading System
Demonstrates all components working together
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_analyzer import NewsAnalyzer
from news_trading_integration import NewsTradingIntegration
from telegram_signal_trader import test_connection
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_news_analyzer():
    """Test the news analyzer component"""
    print("=== Testing News Analyzer ===")

    analyzer = NewsAnalyzer()

    # Test with popular stocks
    test_symbols = ['AAPL', 'GOOGL', 'MSFT']

    for symbol in test_symbols:
        print(f"\n--- Analyzing {symbol} ---")

        try:
            result = analyzer.analyze_symbol(symbol, days_back=2)

            if result:
                print(f"✓ Successfully analyzed {symbol}")

                if result['signal']:
                    signal = result['signal']
                    sentiment = result['sentiment_data']

                    print(f"  Signal: {signal['signal']}")
                    print(f"  Confidence: {signal['confidence']:.3f}")
                    print(f"  Articles: {sentiment['article_count']}")
                    print(f"  Sentiment Score: {sentiment['overall_score']:.3f}")
                    print(f"  Distribution: {sentiment['sentiment_distribution']}")
                else:
                    print(f"  No signal generated (insufficient data)")

                print(f"  News Articles Found: {len(result['news_articles'])}")
            else:
                print(f"✗ Failed to analyze {symbol}")

        except Exception as e:
            print(f"✗ Error analyzing {symbol}: {e}")

    print("\n✓ News Analyzer test complete")

def test_trading_integration():
    """Test the trading integration component"""
    print("\n=== Testing Trading Integration ===")

    integration = NewsTradingIntegration()

    # Test signal generation
    print("Testing signal generation...")
    signals = integration.generate_news_signals(['AAPL'])

    if signals:
        print(f"✓ Generated {len(signals)} signals")
        for signal in signals:
            print(f"  {signal['symbol']}: {signal['signal']} (conf: {signal['confidence']:.3f})")
    else:
        print("ℹ No signals generated (may be due to low news volume)")

    # Test MT5 connection
    print("\nTesting MT5 connection...")
    if test_connection():
        print("✓ MT5 connection successful")
    else:
        print("✗ MT5 connection failed (check credentials)")

    print("\n✓ Trading Integration test complete")

def test_full_system():
    """Test the complete system"""
    print("\n=== Testing Full System ===")

    integration = NewsTradingIntegration()

    # Run a complete trading cycle
    print("Running complete trading cycle...")
    results = integration.run_news_trading_cycle()

    if results:
        print(f"✓ Cycle completed with {len(results)} results")
        for result in results:
            status = "EXECUTED" if result.get('executed', False) else "PENDING"
            print(f"  {status}: {result['symbol']} {result['signal']}")
    else:
        print("ℹ No trading signals generated")

    print("\n✓ Full System test complete")

def main():
    """Main test function"""
    print("News-Based Trading System - Test Suite")
    print("=" * 50)

    try:
        # Test individual components
        test_news_analyzer()
        test_trading_integration()
        test_full_system()

        print("\n" + "=" * 50)
        print("🎉 All tests completed!")
        print("\nNext steps:")
        print("1. Review the test results above")
        print("2. Configure your .env file with real credentials")
        print("3. Run: python news_trading_integration.py --monitor")
        print("4. Monitor logs in trading_bot.log")

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        logger.error(f"Test suite error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
