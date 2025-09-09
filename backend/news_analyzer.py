#!/usr/bin/env python3
"""
News Analyzer Module for Hedge Funder
Fetches news from Yahoo Finance and analyzes sentiment for trading signals
"""

import yfinance as yf
import requests
import logging
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsAnalyzer:
    """Analyzes financial news and generates trading signals"""

    def __init__(self):
        self.sentiment_threshold = float(os.getenv("SENTIMENT_THRESHOLD", "0.1"))
        self.news_lookback_days = int(os.getenv("NEWS_LOOKBACK_DAYS", "7"))
        self.min_news_articles = int(os.getenv("MIN_NEWS_ARTICLES", "3"))

    def get_finnhub_news(self, symbol, days_back=None):
        """Fetch news articles for a symbol from Finnhub API"""
        if days_back is None:
            days_back = self.news_lookback_days

        finnhub_api_key = os.getenv("FINNHUB_API_KEY")
        if not finnhub_api_key:
            logger.warning("Finnhub API key not found, skipping Finnhub news")
            return []

        try:
            logger.info(f"Fetching news for {symbol} from Finnhub")

            # Calculate date range
            from datetime import timezone
            to_date = datetime.now(timezone.utc)
            from_date = to_date - timedelta(days=days_back)

            # Format dates for API
            from_str = from_date.strftime('%Y-%m-%d')
            to_str = to_date.strftime('%Y-%m-%d')

            # Finnhub API endpoint for company news
            url = f"https://finnhub.io/api/v1/company-news"
            params = {
                'symbol': symbol,
                'from': from_str,
                'to': to_str,
                'token': finnhub_api_key
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            news_data = response.json()

            if not news_data:
                logger.info(f"No news found for {symbol} on Finnhub")
                return []

            filtered_news = []
            for article in news_data:
                try:
                    # Convert timestamp to datetime
                    article_date = datetime.fromtimestamp(article.get('datetime', 0), timezone.utc)

                    filtered_news.append({
                        'title': article.get('headline', ''),
                        'summary': article.get('summary', ''),
                        'link': article.get('url', ''),
                        'published': article_date,
                        'publisher': article.get('source', ''),
                        'symbol': symbol
                    })
                except Exception as e:
                    logger.warning(f"Error processing Finnhub article: {e}")
                    continue

            logger.info(f"Found {len(filtered_news)} recent news articles for {symbol} from Finnhub")
            return filtered_news

        except Exception as e:
            logger.error(f"Error fetching news from Finnhub for {symbol}: {e}")
            return []

    def get_yahoo_news(self, symbol, days_back=None):
        """Fetch news articles for a symbol from Yahoo Finance"""
        if days_back is None:
            days_back = self.news_lookback_days

        try:
            logger.info(f"Fetching news for {symbol} from last {days_back} days")

            # Get ticker object
            ticker = yf.Ticker(symbol)

            # Get news
            news = ticker.news

            if not news:
                logger.warning(f"No news found for {symbol}")
                return []

            # Filter news by date (make timezone-aware)
            from datetime import timezone
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            filtered_news = []

            for article in news:
                try:
                    # Handle the nested content structure
                    content = article.get('content', {})
                    pub_date_str = content.get('pubDate', '')

                    if pub_date_str:
                        # Parse ISO format date (e.g., '2025-09-09T10:57:36Z')
                        if pub_date_str.endswith('Z'):
                            pub_date_str = pub_date_str[:-1] + '+00:00'
                        article_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))

                        if article_date >= cutoff_date:
                            filtered_news.append({
                                'title': content.get('title', ''),
                                'summary': content.get('summary', ''),
                                'link': content.get('previewUrl', ''),
                                'published': article_date,
                                'publisher': content.get('provider', {}).get('displayName', ''),
                                'symbol': symbol
                            })
                except Exception as e:
                    logger.warning(f"Error processing article: {e}")
                    continue

            logger.info(f"Found {len(filtered_news)} recent news articles for {symbol}")
            return filtered_news

        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {e}")
            return []

    def get_combined_news(self, symbol, days_back=None):
        """Fetch news from multiple sources with fallback mechanism"""
        if days_back is None:
            days_back = self.news_lookback_days

        all_news = []

        # Try Yahoo Finance first (primary source)
        yahoo_news = self.get_yahoo_news(symbol, days_back)
        if yahoo_news:
            all_news.extend(yahoo_news)
            logger.info(f"Added {len(yahoo_news)} articles from Yahoo Finance")

        # Try Finnhub as secondary source
        finnhub_news = self.get_finnhub_news(symbol, days_back)
        if finnhub_news:
            all_news.extend(finnhub_news)
            logger.info(f"Added {len(finnhub_news)} articles from Finnhub")

        # Remove duplicates based on title
        seen_titles = set()
        unique_news = []
        for article in all_news:
            title = article['title'].lower().strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(article)

        # Sort by publication date (newest first)
        unique_news.sort(key=lambda x: x['published'], reverse=True)

        logger.info(f"Total unique articles for {symbol}: {len(unique_news)}")
        return unique_news

    def analyze_sentiment_simple(self, text):
        """Simple sentiment analysis based on keywords"""
        if not text:
            return 0

        text_lower = text.lower()

        # Positive keywords
        positive_words = ['rise', 'gain', 'up', 'increase', 'growth', 'profit', 'bullish', 'positive', 'strong', 'beat']
        # Negative keywords
        negative_words = ['fall', 'drop', 'down', 'decrease', 'loss', 'decline', 'bearish', 'negative', 'weak', 'miss']

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        # Calculate simple sentiment score
        if positive_count + negative_count == 0:
            return 0

        sentiment_score = (positive_count - negative_count) / (positive_count + negative_count)
        return sentiment_score

    def calculate_overall_sentiment(self, news_articles):
        """Calculate overall sentiment from multiple news articles"""
        if not news_articles:
            return {
                'overall_score': 0,
                'article_count': 0,
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0}
            }

        sentiments = []
        distribution = {'positive': 0, 'neutral': 0, 'negative': 0}

        for article in news_articles:
            # Combine title and summary for analysis
            text = f"{article['title']} {article.get('summary', '')}"
            sentiment_score = self.analyze_sentiment_simple(text)
            sentiments.append(sentiment_score)

            # Classify sentiment
            if sentiment_score > 0.1:
                distribution['positive'] += 1
            elif sentiment_score < -0.1:
                distribution['negative'] += 1
            else:
                distribution['neutral'] += 1

        if sentiments:
            avg_score = sum(sentiments) / len(sentiments)
        else:
            avg_score = 0

        return {
            'overall_score': avg_score,
            'article_count': len(news_articles),
            'sentiment_distribution': distribution
        }

    def generate_signal(self, symbol, sentiment_data):
        """Generate trading signal based on sentiment analysis"""
        score = sentiment_data['overall_score']
        article_count = sentiment_data['article_count']

        # Need minimum number of articles for reliable signal
        if article_count < self.min_news_articles:
            logger.info(f"Insufficient news articles for {symbol}: {article_count}/{self.min_news_articles}")
            return None

        signal = None
        confidence = abs(score)

        if score > self.sentiment_threshold:
            signal = "BUY"
            reason = f"Positive sentiment (score: {score:.3f})"
        elif score < -self.sentiment_threshold:
            signal = "SELL"
            reason = f"Negative sentiment (score: {score:.3f})"
        else:
            signal = "HOLD"
            reason = f"Neutral sentiment (score: {score:.3f})"

        return {
            'symbol': symbol,
            'signal': signal,
            'confidence': confidence,
            'sentiment_score': score,
            'article_count': article_count,
            'reason': reason,
            'timestamp': datetime.now()
        }

    def analyze_symbol(self, symbol, days_back=None):
        """Complete analysis pipeline for a symbol"""
        logger.info(f"Starting analysis for {symbol}")

        # Fetch news from multiple sources
        news_articles = self.get_combined_news(symbol, days_back)

        if not news_articles:
            logger.warning(f"No news data available for {symbol}")
            return None

        # Analyze sentiment
        sentiment_data = self.calculate_overall_sentiment(news_articles)

        # Generate signal
        signal = self.generate_signal(symbol, sentiment_data)

        if signal:
            logger.info(f"Generated signal for {symbol}: {signal['signal']} (confidence: {signal['confidence']:.3f})")

        return {
            'symbol': symbol,
            'news_articles': news_articles,
            'sentiment_data': sentiment_data,
            'signal': signal
        }

    def analyze_multiple_symbols(self, symbols, days_back=None):
        """Analyze multiple symbols"""
        results = {}

        for symbol in symbols:
            try:
                result = self.analyze_symbol(symbol, days_back)
                if result:
                    results[symbol] = result
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {e}")
                continue

        return results

def test_news_analyzer():
    """Test function for the news analyzer"""
    analyzer = NewsAnalyzer()

    # Test with a popular stock
    test_symbols = ['AAPL', 'GOOGL', 'MSFT']

    print("=== News Analyzer Test ===")

    for symbol in test_symbols:
        print(f"\n--- Analyzing {symbol} ---")
        result = analyzer.analyze_symbol(symbol, days_back=3)

        if result and result['signal']:
            signal = result['signal']
            sentiment = result['sentiment_data']

            print(f"Symbol: {signal['symbol']}")
            print(f"Signal: {signal['signal']}")
            print(f"Confidence: {signal['confidence']:.3f}")
            print(f"Articles: {sentiment['article_count']}")
            print(f"Overall Sentiment: {sentiment['overall_score']:.3f}")
            print(f"Distribution: {sentiment['sentiment_distribution']}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_news_analyzer()
