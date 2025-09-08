#!/usr/bin/env python3
"""
Run script for Telegram Signal Trader
Provides easy ways to test and run the trading algorithm
"""

import sys
import os
import argparse
from telegram_signal_trader import process_signal, test_connection, interactive_test

def main():
    parser = argparse.ArgumentParser(description='Telegram Signal Trader')
    parser.add_argument('--signal', '-s', help='Process a single trading signal')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--test', '-t', action='store_true', help='Test MT5 connection')
    parser.add_argument('--demo', '-d', action='store_true', help='Run demo signals (no real trades)')

    args = parser.parse_args()

    if args.test:
        print("Testing MT5 connection...")
        success = test_connection()
        sys.exit(0 if success else 1)

    elif args.signal:
        print(f"Processing signal: {args.signal}")
        process_signal(args.signal)

    elif args.interactive:
        print("Starting interactive mode...")
        interactive_test()

    elif args.demo:
        print("Running demo signals (simulation mode)...")
        demo_signals = [
            "BUY EURUSD SL=1.0500 TP=1.0700",
            "SELL GBPUSD SL=1.2500 TP=1.2300",
            "BUY USDJPY SL=150.00 TP=152.00"
        ]

        for signal in demo_signals:
            print(f"\n--- Processing Demo Signal: {signal} ---")
            process_signal(signal)
            print("Demo signal processed (no real trade placed)")

    else:
        print("Telegram Signal Trader")
        print("Usage:")
        print("  python run_trader.py --test                    # Test MT5 connection")
        print("  python run_trader.py --signal 'BUY EURUSD SL=1.0500 TP=1.0700'  # Process single signal")
        print("  python run_trader.py --interactive            # Interactive mode")
        print("  python run_trader.py --demo                   # Run demo signals")
        print("\nMake sure to set up your .env file with MT5 credentials!")

if __name__ == "__main__":
    main()
