#!/usr/bin/env python3
"""
Integration module for News-based Trading
Combines news analysis with existing trading system
"""

import logging
import time
from datetime import datetime
from news_analyzer import NewsAnalyzer
from telegram_signal_trader import process_signal, test_connection
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsTradingIntegration:
    """Integrates news analysis with trading execution"""

    def __init__(self):
        self.news_analyzer = NewsAnalyzer()
        self.analysis_interval = int(os.getenv("ANALYSIS_INTERVAL_MINUTES", "60"))  # Default 1 hour
        self.symbols_to_monitor = os.getenv("MONITOR_SYMBOLS", "AAPL,GOOGL,MSFT,TSLA").split(",")
        self.auto_trade = os.getenv("AUTO_TRADE", "false").lower() == "true"

    def generate_news_signals(self, symbols=None):
        """Generate trading signals based on news analysis"""
        if symbols is None:
            symbols = self.symbols_to_monitor

        logger.info(f"Analyzing news for symbols: {symbols}")

        # Analyze all symbols
        analysis_results = self.news_analyzer.analyze_multiple_symbols(symbols, days_back=1)

        signals = []

        for symbol, result in analysis_results.items():
            if result and result['signal']:
                signal_data = result['signal']

                # Only process BUY/SELL signals (ignore HOLD)
                if signal_data['signal'] in ['BUY', 'SELL']:
                    # Format for existing trading system
                    formatted_signal = f"{signal_data['signal']} {symbol} SL=0.00 TP=0.00"

                    signals.append({
                        'symbol': symbol,
                        'signal': signal_data['signal'],
                        'confidence': signal_data['confidence'],
                        'reason': signal_data['reason'],
                        'formatted_signal': formatted_signal,
                        'article_count': signal_data['article_count']
                    })

        logger.info(f"Generated {len(signals)} trading signals from news analysis")
        return signals

    def execute_signals(self, signals):
        """Execute trading signals using existing MT5 system"""
        executed_signals = []

        for signal in signals:
            try:
                logger.info(f"Processing signal: {signal['formatted_signal']}")

                if self.auto_trade:
                    # Execute the trade
                    process_signal(signal['formatted_signal'])
                    signal['executed'] = True
                    signal['execution_time'] = datetime.now()
                    logger.info(f"Executed signal: {signal['formatted_signal']}")
                else:
                    # Just log the signal
                    signal['executed'] = False
                    logger.info(f"Signal ready for manual execution: {signal['formatted_signal']}")

                executed_signals.append(signal)

            except Exception as e:
                logger.error(f"Error executing signal {signal['formatted_signal']}: {e}")
                signal['executed'] = False
                signal['error'] = str(e)
                executed_signals.append(signal)

        return executed_signals

    def run_news_trading_cycle(self):
        """Run one complete news analysis and trading cycle"""
        logger.info("=== Starting News Trading Cycle ===")

        try:
            # Step 1: Generate signals from news
            signals = self.generate_news_signals()

            if not signals:
                logger.info("No trading signals generated from news analysis")
                return []

            # Step 2: Execute signals
            executed_signals = self.execute_signals(signals)

            # Step 3: Log results
            successful_trades = [s for s in executed_signals if s.get('executed', False)]
            failed_trades = [s for s in executed_signals if not s.get('executed', False)]

            logger.info(f"Cycle complete: {len(successful_trades)} successful, {len(failed_trades)} failed")

            return executed_signals

        except Exception as e:
            logger.error(f"Error in news trading cycle: {e}")
            return []

    def start_continuous_monitoring(self):
        """Start continuous monitoring and trading based on news"""
        logger.info("=== Starting Continuous News Trading Monitor ===")
        logger.info(f"Analysis interval: {self.analysis_interval} minutes")
        logger.info(f"Auto-trade enabled: {self.auto_trade}")
        logger.info(f"Monitored symbols: {self.symbols_to_monitor}")

        # Test MT5 connection first
        if not test_connection():
            logger.error("MT5 connection test failed. Please check your credentials.")
            return

        cycle_count = 0

        try:
            while True:
                cycle_count += 1
                logger.info(f"=== Cycle {cycle_count} ===")

                # Run trading cycle
                results = self.run_news_trading_cycle()

                # Log summary
                if results:
                    for result in results:
                        status = "EXECUTED" if result.get('executed', False) else "PENDING"
                        logger.info(f"{status}: {result['symbol']} {result['signal']} (conf: {result['confidence']:.3f})")

                # Wait for next cycle
                logger.info(f"Waiting {self.analysis_interval} minutes until next analysis...")
                time.sleep(self.analysis_interval * 60)

        except KeyboardInterrupt:
            logger.info("Continuous monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous monitoring: {e}")

def test_integration():
    """Test the news trading integration"""
    integration = NewsTradingIntegration()

    print("=== News Trading Integration Test ===")

    # Test MT5 connection
    print("Testing MT5 connection...")
    if test_connection():
        print("✓ MT5 connection successful")
    else:
        print("✗ MT5 connection failed")
        return

    # Test news signal generation
    print("\nTesting news signal generation...")
    signals = integration.generate_news_signals(['AAPL', 'GOOGL'])

    if signals:
        print(f"✓ Generated {len(signals)} signals:")
        for signal in signals:
            print(f"  - {signal['symbol']}: {signal['signal']} (confidence: {signal['confidence']:.3f})")
    else:
        print("✗ No signals generated")

    # Test signal execution (without actual trading)
    print("\nTesting signal execution (simulation)...")
    if signals:
        # Temporarily disable auto-trade for testing
        original_auto_trade = integration.auto_trade
        integration.auto_trade = False

        executed = integration.execute_signals(signals[:1])  # Test with first signal
        print(f"✓ Signal execution test: {executed[0]['executed']}")

        # Restore original setting
        integration.auto_trade = original_auto_trade

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_integration()
    elif len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        integration = NewsTradingIntegration()
        integration.start_continuous_monitoring()
    else:
        print("News Trading Integration")
        print("Usage:")
        print("  python news_trading_integration.py --test      # Run tests")
        print("  python news_trading_integration.py --monitor   # Start continuous monitoring")
        print("  python news_trading_integration.py             # Show this help")
