#!/usr/bin/env python3
"""
Test Finnhub API Integration
Tests news fetching, sentiment analysis, and trading signals from Finnhub
"""

import os
import logging
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FinnhubClient:
    """Finnhub API client for news and market data"""

    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY')
        self.base_url = "https://finnhub.io/api/v1"

        if not self.api_key:
            logger.warning("Finnhub API key not found in environment variables")

    def get_company_news(self, symbol, from_date=None, to_date=None):
        """Get company news for a specific symbol"""
        if not self.api_key:
            logger.error("Finnhub API key not configured")
            return []

        try:
            if from_date is None:
                from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            if to_date is None:
                to_date = datetime.now().strftime('%Y-%m-%d')

            url = f"{self.base_url}/company-news"
            params = {
                'symbol': symbol,
                'from': from_date,
                'to': to_date,
                'token': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            news_data = response.json()

            # Format news articles
            articles = []
            for article in news_data[:20]:  # Limit to 20 articles
                articles.append({
                    'title': article.get('headline', ''),
                    'summary': article.get('summary', ''),
                    'source': article.get('source', ''),
                    'url': article.get('url', ''),
                    'published': datetime.fromtimestamp(article.get('datetime', 0)).isoformat(),
                    'symbol': symbol
                })

            logger.info(f"Fetched {len(articles)} news articles for {symbol}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching company news: {e}")
            return []

    def get_market_news(self, category='general'):
        """Get general market news"""
        if not self.api_key:
            logger.error("Finnhub API key not configured")
            return []

        try:
            url = f"{self.base_url}/news"
            params = {
                'category': category,
                'token': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            news_data = response.json()

            # Format news articles
            articles = []
            for article in news_data[:10]:  # Limit to 10 articles
                articles.append({
                    'title': article.get('headline', ''),
                    'summary': article.get('summary', ''),
                    'source': article.get('source', ''),
                    'url': article.get('url', ''),
                    'published': datetime.fromtimestamp(article.get('datetime', 0)).isoformat(),
                    'category': category
                })

            logger.info(f"Fetched {len(articles)} market news articles")
            return articles

        except Exception as e:
            logger.error(f"Error fetching market news: {e}")
            return []

    def get_quote(self, symbol):
        """Get current quote for a symbol"""
        if not self.api_key:
            logger.error("Finnhub API key not configured")
            return None

        try:
            url = f"{self.base_url}/quote"
            params = {
                'symbol': symbol,
                'token': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            quote_data = response.json()

            return {
                'symbol': symbol,
                'current_price': quote_data.get('c', 0),
                'change': quote_data.get('d', 0),
                'change_percent': quote_data.get('dp', 0),
                'high': quote_data.get('h', 0),
                'low': quote_data.get('l', 0),
                'open': quote_data.get('o', 0),
                'previous_close': quote_data.get('pc', 0),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {e}")
            return None

    def get_earnings_calendar(self, symbol=None, from_date=None, to_date=None):
        """Get earnings calendar"""
        if not self.api_key:
            logger.error("Finnhub API key not configured")
            return []

        try:
            if from_date is None:
                from_date = datetime.now().strftime('%Y-%m-%d')
            if to_date is None:
                to_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')

            url = f"{self.base_url}/calendar/earnings"
            params = {
                'from': from_date,
                'to': to_date,
                'token': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            earnings_data = response.json()

            earnings = []
            for earning in earnings_data.get('earningsCalendar', []):
                if symbol and earning.get('symbol') != symbol:
                    continue

                earnings.append({
                    'symbol': earning.get('symbol'),
                    'date': earning.get('date'),
                    'eps_estimate': earning.get('epsEstimate'),
                    'eps_actual': earning.get('epsActual'),
                    'revenue_estimate': earning.get('revenueEstimate'),
                    'revenue_actual': earning.get('revenueActual'),
                    'hour': earning.get('hour')
                })

            logger.info(f"Fetched {len(earnings)} earnings events")
            return earnings

        except Exception as e:
            logger.error(f"Error fetching earnings calendar: {e}")
            return []

def test_finnhub_connection():
    """Test Finnhub API connection"""
    client = FinnhubClient()

    print("🔍 Testing Finnhub API connection...")

    # Test company news
    print("\n📈 Testing company news fetch...")
    news = client.get_company_news('AAPL')
    if news:
        print(f"✅ Fetched {len(news)} news articles for AAPL")
        print(f"Sample article: {news[0]['title'][:50]}...")
    else:
        print("❌ Failed to fetch company news")

    # Test market news
    print("\n🌍 Testing market news fetch...")
    market_news = client.get_market_news()
    if market_news:
        print(f"✅ Fetched {len(market_news)} market news articles")
        print(f"Sample article: {market_news[0]['title'][:50]}...")
    else:
        print("❌ Failed to fetch market news")

    # Test quote
    print("\n💰 Testing quote fetch...")
    quote = client.get_quote('AAPL')
    if quote:
        print(f"✅ AAPL Quote: ${quote['current_price']:.2f} ({quote['change_percent']:+.2f}%)")
    else:
        print("❌ Failed to fetch quote")

    # Test earnings
    print("\n📊 Testing earnings calendar...")
    earnings = client.get_earnings_calendar('AAPL')
    if earnings:
        print(f"✅ Found {len(earnings)} upcoming earnings for AAPL")
        if earnings:
            print(f"Next earnings: {earnings[0]['date']}")
    else:
        print("❌ Failed to fetch earnings calendar")

    print("\n🎯 Finnhub integration test completed!")

def analyze_news_sentiment(news_articles):
    """Basic sentiment analysis for news articles"""
    if not news_articles:
        return {'sentiment': 'neutral', 'confidence': 0.0}

    # Simple keyword-based sentiment analysis
    positive_words = ['rise', 'gain', 'up', 'bullish', 'beat', 'strong', 'growth', 'profit', 'success']
    negative_words = ['fall', 'drop', 'down', 'bearish', 'miss', 'weak', 'decline', 'loss', 'fail']

    total_positive = 0
    total_negative = 0

    for article in news_articles:
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)

        total_positive += positive_count
        total_negative += negative_count

    total_words = total_positive + total_negative

    if total_words == 0:
        return {'sentiment': 'neutral', 'confidence': 0.0}

    sentiment_score = (total_positive - total_negative) / total_words

    if sentiment_score > 0.1:
        sentiment = 'positive'
    elif sentiment_score < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    confidence = min(abs(sentiment_score), 1.0)

    return {
        'sentiment': sentiment,
        'confidence': confidence,
        'positive_words': total_positive,
        'negative_words': total_negative,
        'total_articles': len(news_articles)
    }

def generate_trading_signal(symbol, news_sentiment, quote_data=None):
    """Generate trading signal based on news sentiment and quote data"""
    if not news_sentiment:
        return {'signal': 'HOLD', 'confidence': 0.0, 'reason': 'No sentiment data'}

    sentiment = news_sentiment['sentiment']
    confidence = news_sentiment['confidence']

    # Simple signal generation logic
    if sentiment == 'positive' and confidence > 0.3:
        signal = 'BUY'
        reason = f"Positive news sentiment (confidence: {confidence:.2f})"
    elif sentiment == 'negative' and confidence > 0.3:
        signal = 'SELL'
        reason = f"Negative news sentiment (confidence: {confidence:.2f})"
    else:
        signal = 'HOLD'
        reason = f"Neutral or low confidence sentiment (confidence: {confidence:.2f})"

    return {
        'symbol': symbol,
        'signal': signal,
        'confidence': confidence,
        'reason': reason,
        'sentiment_data': news_sentiment,
        'quote_data': quote_data,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    # Run connection test
    test_finnhub_connection()

    # Test sentiment analysis
    print("\n🧠 Testing sentiment analysis...")
    client = FinnhubClient()
    news = client.get_company_news('TSLA')

    if news:
        sentiment = analyze_news_sentiment(news)
        print(f"TSLA Sentiment: {sentiment}")

        signal = generate_trading_signal('TSLA', sentiment)
        print(f"Trading Signal: {signal['signal']} (confidence: {signal['confidence']:.2f})")
        print(f"Reason: {signal['reason']}")
    else:
        print("❌ No news data for sentiment analysis")
