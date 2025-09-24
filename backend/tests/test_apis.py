import os
import sys
import requests
import pandas as pd
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the module with proper handling of spaces in filename
import importlib.util
spec = importlib.util.spec_from_file_location("market_analysis", os.path.join(os.path.dirname(__file__), '..', 'market_analysis_algorithm', 'market_analysis.py'))
market_analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(market_analysis)
load_config = market_analysis.load_config

def test_finnhub_api():
    """Test Finnhub API for real-time prices"""
    config = load_config()
    api_key = config['api_keys']['finnhub']
    ticker = 'AAPL'

    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
        response = requests.get(url)
        data = response.json()

        if 'c' in data:
            print(f"✅ Finnhub API working for {ticker}")
            print(f"   Current Price: {data.get('c', 0)}")
            return True
        else:
            print(f"❌ Finnhub API error for {ticker}: {data}")
            return False
    except Exception as e:
        print(f"❌ Finnhub API exception: {str(e)}")
        return False

def test_alpha_vantage_api():
    """Test Alpha Vantage API for historical data"""
    config = load_config()
    api_key = config['api_keys']['alpha_vantage']
    ticker = 'AAPL'

    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}&outputsize=compact"
        response = requests.get(url)
        data = response.json()

        if 'Time Series (Daily)' in data:
            df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
            print(f"✅ Alpha Vantage API working for {ticker}")
            print(f"   Data points: {len(df)}")
            return True
        else:
            print(f"❌ Alpha Vantage API error for {ticker}: {data}")
            return False
    except Exception as e:
        print(f"❌ Alpha Vantage API exception: {str(e)}")
        return False

def test_twelve_data_api():
    """Test Twelve Data API for intraday data"""
    config = load_config()
    api_key = config['api_keys']['twelve_data']
    ticker = 'AAPL'
    interval = '1min'

    try:
        url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval={interval}&outputsize=10&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        if 'values' in data:
            df = pd.DataFrame(data['values'])
            print(f"✅ Twelve Data API working for {ticker}")
            print(f"   Data points: {len(df)}")
            return True
        else:
            print(f"❌ Twelve Data API error for {ticker}: {data}")
            return False
    except Exception as e:
        print(f"❌ Twelve Data API exception: {str(e)}")
        return False

def main():
    print("Testing API integrations...")
    print("=" * 50)

    results = []

    print("\n1. Testing Finnhub API (Real-time prices):")
    results.append(test_finnhub_api())

    print("\n2. Testing Alpha Vantage API (Historical data):")
    results.append(test_alpha_vantage_api())

    print("\n3. Testing Twelve Data API (Intraday data):")
    results.append(test_twelve_data_api())

    print("\n" + "=" * 50)
    print("Summary:")
    print(f"✅ Passed: {sum(results)}/3")
    print(f"❌ Failed: {3 - sum(results)}/3")

    if all(results):
        print("🎉 All APIs are working correctly!")
        return 0
    else:
        print("⚠️  Some APIs failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
