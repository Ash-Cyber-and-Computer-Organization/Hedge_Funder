#!/usr/bin/env python3
"""
Test script for Telegram Signal Trader
Demonstrates various signal processing scenarios
"""

from telegram_signal_trader import process_signal, test_connection
import time

def run_tests():
    """Run comprehensive tests for the trading algorithm"""

    print("=== Telegram Signal Trader - Test Suite ===\n")

    # Test 1: Connection Test
    print("1. Testing MT5 Connection...")
    if test_connection():
        print("✓ MT5 connection successful\n")
    else:
        print("✗ MT5 connection failed - check your credentials\n")
        return

    # Test 2: Valid Signals
    print("2. Testing Valid Signals...")
    valid_signals = [
        "BUY EURUSD SL=1.0500 TP=1.0700",
        "SELL GBPUSD SL=1.2500 TP=1.2300",
        "BUY USDJPY SL=150.00 TP=152.00"
    ]

    for signal in valid_signals:
        print(f"Processing: {signal}")
        process_signal(signal)
        time.sleep(1)  # Brief pause between signals

    print()

    # Test 3: Invalid Signals
    print("3. Testing Invalid Signals...")
    invalid_signals = [
        "BUY EURUSD",  # Missing SL/TP
        "HOLD EURUSD SL=1.0500 TP=1.0700",  # Invalid action
        "BUY INVALID_SYMBOL SL=1.0500 TP=1.0700",  # Invalid symbol
        "BUY EURUSD SL=INVALID TP=1.0700",  # Invalid SL value
    ]

    for signal in invalid_signals:
        print(f"Processing invalid signal: {signal}")
        process_signal(signal)
        time.sleep(1)

    print("\n=== Test Suite Complete ===")
    print("Check trading_bot.log for detailed logs")
    print("Check console output for real-time results")

if __name__ == "__main__":
    run_tests()
