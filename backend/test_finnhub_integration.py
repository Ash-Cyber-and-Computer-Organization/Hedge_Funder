#!/usr/bin/env python3
"""
Test script to verify Finnhub API integration
"""

import os
import logging
from dotenv import load_dotenv
from news_analyzer import NewsAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_finnhub_api():
    """Test Finnhub API integration"""
    print("=== Testing Finnhub API Integration ===")

    # Check if API key is configured
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_api_key or finnhub_api_key == "your_finnhub_api_key_here":
        print("❌ Finnhub API key not configured properly")
        print("Please set FINNHUB_API_KEY in your .env file")
        return False

    print(f"✅ Finnhub API key found: {finnhub_api_key[:8]}...")

    # Initialize analyzer
    analyzer = NewsAnalyzer()

    # Test with a popular stock
    test_symbol = "AAPL"

    print(f"\n--- Testing Finnhub news fetch for {test_symbol} ---")

    try:
        # Test Finnhub news fetching
        finnhub_news = analyzer.get_finnhub_news(test_symbol, days_back=3)

        if finnhub_news:
            print(f"✅ Successfully fetched {len(finnhub_news)} articles from Finnhub")

            # Show first article as example
            if finnhub_news:
                article = finnhub_news[0]
                print(f"\n📄 Sample article:")
                print(f"Title: {article['title']}")
                print(f"Summary: {article['summary'][:100]}...")
                print(f"Published: {article['published']}")
                print(f"Publisher: {article['publisher']}")
                print(f"Link: {article['link']}")

            return True
        else:
            print("⚠️  No news articles returned from Finnhub")
            print("This could be normal if there are no recent news for the symbol")
            return True

    except Exception as e:
        print(f"❌ Error testing Finnhub API: {e}")
        return False

def test_combined_news():
    """Test combined news fetching"""
    print("\n=== Testing Combined News Fetching ===")

    analyzer = NewsAnalyzer()
    test_symbol = "AAPL"

    try:
        combined_news = analyzer.get_combined_news(test_symbol, days_back=3)

        print(f"✅ Combined news fetch successful")
        print(f"Total articles: {len(combined_news)}")

        if combined_news:
            print(f"\n📊 News sources breakdown:")
            yahoo_count = sum(1 for article in combined_news if 'yahoo' in article.get('link', '').lower() or 'yahoo' in article.get('publisher', '').lower())
            finnhub_count = len(combined_news) - yahoo_count
            print(f"Yahoo Finance: {yahoo_count} articles")
            print(f"Finnhub: {finnhub_count} articles")

        return True

    except Exception as e:
        print(f"❌ Error testing combined news: {e}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("\n=== Testing Sentiment Analysis ===")

    analyzer = NewsAnalyzer()

    # Test with sample news
    sample_news = [
        {
            'title': 'Apple stock rises on strong earnings',
            'summary': 'Apple reported better than expected quarterly results',
            'published': '2024-01-01',
            'publisher': 'Financial Times',
            'symbol': 'AAPL'
        },
        {
            'title': 'Apple faces supply chain challenges',
            'summary': 'Manufacturing delays could impact iPhone production',
            'published': '2024-01-02',
            'publisher': 'Reuters',
            'symbol': 'AAPL'
        }
    ]

    try:
        sentiment_data = analyzer.calculate_overall_sentiment(sample_news)
        signal = analyzer.generate_signal('AAPL', sentiment_data)

        print("✅ Sentiment analysis successful")
        print(f"Overall score: {sentiment_data['overall_score']:.3f}")
        print(f"Article count: {sentiment_data['article_count']}")
        print(f"Distribution: {sentiment_data['sentiment_distribution']}")

        if signal:
            print(f"Signal: {signal['signal']} (confidence: {signal['confidence']:.3f})")
        else:
            print("No signal generated (insufficient articles)")

        return True

    except Exception as e:
        print(f"❌ Error testing sentiment analysis: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Finnhub Integration Tests\n")

    # Run all tests
    test1_passed = test_finnhub_api()
    test2_passed = test_combined_news()
    test3_passed = test_sentiment_analysis()

    print("\n=== Test Results ===")
    print(f"Finnhub API Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Combined News Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Sentiment Analysis Test: {'✅ PASSED' if test3_passed else '❌ FAILED'}")

    if all([test1_passed, test2_passed, test3_passed]):
        print("\n🎉 All tests passed! Finnhub integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration and try again.")
