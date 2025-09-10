#!/usr/bin/env python3
"""
Multi-Source News Aggregator
Combines multiple free news APIs for comprehensive market coverage
"""

import os
import logging
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import feedparser
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsAggregator:
    """Aggregates news from multiple free APIs for comprehensive coverage"""

    def __init__(self):
        self.sources = {
            'finnhub': FinnhubNewsClient(),
            'newsapi': NewsAPIClient(),
            'alphavantage': AlphaVantageNewsClient(),
            'yahoo': YahooFinanceNewsClient(),
            'google': GoogleNewsClient()
        }

    def get_comprehensive_news(self, symbol, days_back=3):
        """Get news from all available sources"""
        all_news = []
        source_stats = {}

        for source_name, client in self.sources.items():
            try:
                logger.info(f"Fetching news from {source_name} for {symbol}")
                news = client.get_news(symbol, days_back)
                all_news.extend(news)
                source_stats[source_name] = len(news)
                logger.info(f"✅ {source_name}: {len(news)} articles")

                # Rate limiting
                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"❌ {source_name} failed: {e}")
                source_stats[source_name] = 0

        # Remove duplicates based on title similarity
        unique_news = self._remove_duplicates(all_news)

        logger.info(f"📊 Total articles: {len(all_news)} → {len(unique_news)} unique")

        return {
            'articles': unique_news,
            'total_articles': len(unique_news),
            'source_breakdown': source_stats,
            'timestamp': datetime.now().isoformat()
        }

    def _remove_duplicates(self, articles):
        """Remove duplicate articles based on title similarity"""
        if not articles:
            return []

        unique_articles = []

        for article in articles:
            title = article.get('title', '').lower().strip()

            # Check if similar title already exists
            is_duplicate = False
            for existing in unique_articles:
                existing_title = existing.get('title', '').lower().strip()

                # Simple similarity check (80% overlap)
                if self._title_similarity(title, existing_title) > 0.8:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_articles.append(article)

        return unique_articles

    def _title_similarity(self, title1, title2):
        """Calculate title similarity using word overlap"""
        words1 = set(title1.split())
        words2 = set(title2.split())

        if not words1 or not words2:
            return 0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0

class FinnhubNewsClient:
    """Finnhub News API Client"""

    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY')
        self.base_url = "https://finnhub.io/api/v1"

    def get_news(self, symbol, days_back=3):
        if not self.api_key:
            return []

        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
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

            articles = []
            for article in news_data[:15]:
                articles.append({
                    'title': article.get('headline', ''),
                    'summary': article.get('summary', ''),
                    'source': article.get('source', 'Finnhub'),
                    'url': article.get('url', ''),
                    'published': datetime.fromtimestamp(article.get('datetime', 0)).isoformat(),
                    'symbol': symbol,
                    'api_source': 'finnhub'
                })

            return articles

        except Exception as e:
            logger.error(f"Finnhub error: {e}")
            return []

class NewsAPIClient:
    """NewsAPI.org Client"""

    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.base_url = "https://newsapi.org/v2"

    def get_news(self, symbol, days_back=3):
        if not self.api_key:
            return []

        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

            # Search for company news
            query = f'"{symbol}" stock OR "{symbol}" shares OR "{symbol}" market'
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'from': from_date,
                'sortBy': 'publishedAt',
                'apiKey': self.api_key,
                'language': 'en',
                'pageSize': 20
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', ''),
                    'summary': article.get('description', ''),
                    'source': article.get('source', {}).get('name', 'NewsAPI'),
                    'url': article.get('url', ''),
                    'published': article.get('publishedAt', ''),
                    'symbol': symbol,
                    'api_source': 'newsapi'
                })

            return articles

        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return []

class AlphaVantageNewsClient:
    """Alpha Vantage News API Client"""

    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = "https://www.alphavantage.co/query"

    def get_news(self, symbol, days_back=3):
        if not self.api_key:
            return []

        try:
            url = self.base_url
            params = {
                'function': 'NEWS_SENTIMENT',
                'tickers': symbol,
                'apikey': self.api_key,
                'limit': 20
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            articles = []
            for article in data.get('feed', []):
                articles.append({
                    'title': article.get('title', ''),
                    'summary': article.get('summary', ''),
                    'source': article.get('source', 'Alpha Vantage'),
                    'url': article.get('url', ''),
                    'published': article.get('time_published', ''),
                    'symbol': symbol,
                    'api_source': 'alphavantage',
                    'sentiment_score': article.get('overall_sentiment_score', 0)
                })

            return articles

        except Exception as e:
            logger.error(f"Alpha Vantage error: {e}")
            return []

class YahooFinanceNewsClient:
    """Yahoo Finance News Client"""

    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v7/finance/chart/"

    def get_news(self, symbol, days_back=3):
        try:
            # Yahoo Finance doesn't have a direct news API, but we can use RSS feeds
            rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

            feed = feedparser.parse(rss_url)

            articles = []
            for entry in feed.entries[:10]:
                articles.append({
                    'title': entry.get('title', ''),
                    'summary': entry.get('summary', ''),
                    'source': 'Yahoo Finance',
                    'url': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'symbol': symbol,
                    'api_source': 'yahoo'
                })

            return articles

        except Exception as e:
            logger.error(f"Yahoo Finance error: {e}")
            return []

class GoogleNewsClient:
    """Google News RSS Client"""

    def __init__(self):
        self.base_url = "https://news.google.com/rss"

    def get_news(self, symbol, days_back=3):
        try:
            # Use Google News RSS for company-specific news
            search_term = f'{symbol} stock'
            rss_url = f"https://news.google.com/rss/search?q={search_term}&hl=en-US&gl=US&ceid=US:en"

            feed = feedparser.parse(rss_url)

            articles = []
            for entry in feed.entries[:15]:
                articles.append({
                    'title': entry.get('title', ''),
                    'summary': entry.get('summary', ''),
                    'source': 'Google News',
                    'url': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'symbol': symbol,
                    'api_source': 'google'
                })

            return articles

        except Exception as e:
            logger.error(f"Google News error: {e}")
            return []

def test_news_aggregator():
    """Test the news aggregator with multiple sources"""
    aggregator = NewsAggregator()

    print("📰 Testing Multi-Source News Aggregator...")

    # Test with popular stocks
    test_symbols = ['AAPL', 'TSLA', 'GOOGL', 'MSFT']

    for symbol in test_symbols:
        print(f"\n📊 Testing {symbol}...")

        try:
            result = aggregator.get_comprehensive_news(symbol, days_back=2)

            print(f"✅ {symbol}: {result['total_articles']} unique articles")
            print(f"📈 Source breakdown: {result['source_breakdown']}")

            if result['articles']:
                print(f"📝 Sample: {result['articles'][0]['title'][:60]}...")
                print(f"🔗 Source: {result['articles'][0]['api_source']}")

        except Exception as e:
            print(f"❌ {symbol} failed: {e}")

        time.sleep(1)  # Rate limiting

    print("\n🎯 News aggregator test completed!")

if __name__ == '__main__':
    test_news_aggregator()
