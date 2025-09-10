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
from newsapi import NewsApiClient
import feedparser
from bs4 import BeautifulSoup

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
        if not finnhub_api_key or finnhub_api_key == "your_finnhub_api_key_here":
            logger.warning("Finnhub API key not configured properly")
            return []

        try:
            logger.info(f"Fetching news for {symbol} from Finnhub (last {days_back} days)")

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

            logger.info(f"Making request to Finnhub: {url} with params {params}")

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            news_data = response.json()

            if not news_data or not isinstance(news_data, list):
                logger.info(f"No news data returned from Finnhub for {symbol}")
                return []

            logger.info(f"Finnhub returned {len(news_data)} raw articles for {symbol}")

            filtered_news = []
            for article in news_data:
                try:
                    # Convert timestamp to datetime
                    article_date = datetime.fromtimestamp(article.get('datetime', 0), timezone.utc)

                    # Only include articles within our date range
                    if article_date >= from_date:
                        filtered_news.append({
                            'title': article.get('headline', '').strip(),
                            'summary': article.get('summary', '').strip(),
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

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching from Finnhub for {symbol}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching news from Finnhub for {symbol}: {e}")
            return []

    def get_yahoo_news(self, symbol, days_back=None):
        """Fetch news articles for a symbol from Yahoo Finance with yfinance 0.2.40 compatible method"""
        if days_back is None:
            days_back = self.news_lookback_days

        try:
            logger.info(f"Fetching news for {symbol} from last {days_back} days")

            # Use yfinance Ticker with new news method
            ticker = yf.Ticker(symbol)

            # Try multiple methods to get news from Yahoo Finance
            news = None

            # Method 1: Try the new get_news() method
            try:
                news = ticker.get_news()
                logger.info(f"Successfully retrieved {len(news) if news else 0} news items from Yahoo Finance for {symbol} using get_news()")
            except Exception as e:
                logger.warning(f"Failed to get news from yfinance for {symbol} using get_news(): {e}")

            # Method 2: Try the legacy news property
            if not news:
                try:
                    news = ticker.news
                    logger.info(f"Successfully retrieved {len(news) if news else 0} news items from Yahoo Finance for {symbol} using legacy news property")
                except Exception as e:
                    logger.warning(f"Failed to get news from yfinance for {symbol} using legacy news property: {e}")

            # Method 3: Try direct API call
            if not news:
                try:
                    news = self._fetch_yahoo_news_direct(symbol, days_back)
                    logger.info(f"Successfully retrieved {len(news) if news else 0} news items from Yahoo Finance for {symbol} using direct API")
                except Exception as e:
                    logger.warning(f"Failed to get news from yfinance for {symbol} using direct API: {e}")
                    return []

            # Check if news is valid
            if not news or not isinstance(news, list):
                logger.warning(f"No valid news data returned for {symbol} from Yahoo Finance")
                return []

            # Filter news by date
            cutoff_date = datetime.now() - timedelta(days=days_back)
            filtered_news = []

            for article in news:
                try:
                    # article is expected to be a dict with keys like 'title', 'publisher', 'link', 'providerPublishTime'
                    pub_time = article.get('providerPublishTime', 0)
                    if pub_time > 0:
                        article_date = datetime.fromtimestamp(pub_time)
                        if article_date >= cutoff_date:
                            title = article.get('title', '').strip()
                            if title:  # Only add if title exists
                                filtered_news.append({
                                    'title': title,
                                    'summary': article.get('summary', '').strip() if 'summary' in article else '',
                                    'link': article.get('link', ''),
                                    'published': article_date,
                                    'publisher': article.get('publisher', ''),
                                    'symbol': symbol
                                })
                except Exception as e:
                    logger.warning(f"Error processing Yahoo article: {e}")
                    continue

            logger.info(f"Found {len(filtered_news)} recent news articles for {symbol} from Yahoo")
            return filtered_news

        except Exception as e:
            logger.error(f"Error fetching news for {symbol} from Yahoo Finance: {e}")
            return []

    def get_yahoo_news_alternative(self, symbol, days_back=None):
        """Alternative method to fetch Yahoo Finance news using direct API calls"""
        if days_back is None:
            days_back = self.news_lookback_days

        try:
            logger.info(f"Trying alternative Yahoo Finance news fetch for {symbol}")

            # Use yfinance's internal methods with more control
            ticker = yf.Ticker(symbol)

            # Try to get news using different approach
            try:
                # Get news data directly
                news_data = ticker._get_news()

                if news_data and isinstance(news_data, list):
                    logger.info(f"Alternative method found {len(news_data)} news items")
                    return self._process_yahoo_news_data(news_data, symbol, days_back)

            except Exception as e:
                logger.warning(f"Alternative method failed: {e}")

            # If all else fails, return empty list
            logger.warning(f"All Yahoo Finance methods failed for {symbol}")
            return []

        except Exception as e:
            logger.error(f"Error in alternative Yahoo news fetch for {symbol}: {e}")
            return []

    def _process_yahoo_news_data(self, news_data, symbol, days_back):
        """Process raw Yahoo news data into standardized format"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_news = []

        for article in news_data:
            try:
                if isinstance(article, dict):
                    # Try different date fields
                    article_date = None

                    # Try various date fields
                    date_fields = ['pubDate', 'published', 'date', 'datetime']
                    for field in date_fields:
                        if field in article:
                            date_value = article[field]
                            if isinstance(date_value, str):
                                try:
                                    if date_value.endswith('Z'):
                                        date_value = date_value[:-1] + '+00:00'
                                    article_date = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                                    break
                                except:
                                    continue
                            elif isinstance(date_value, (int, float)):
                                try:
                                    article_date = datetime.fromtimestamp(date_value)
                                    break
                                except:
                                    continue

                    # If no date found, use current time
                    if article_date is None:
                        article_date = datetime.now()

                    if article_date >= cutoff_date:
                        # Try different title fields
                        title = ''
                        title_fields = ['title', 'headline', 'name']
                        for field in title_fields:
                            if field in article and article[field]:
                                title = str(article[field]).strip()
                                break

                        if title:
                            filtered_news.append({
                                'title': title,
                                'summary': str(article.get('summary', article.get('description', ''))).strip(),
                                'link': str(article.get('link', article.get('url', ''))),
                                'published': article_date,
                                'publisher': str(article.get('publisher', article.get('source', ''))),
                                'symbol': symbol
                            })

            except Exception as e:
                logger.warning(f"Error processing alternative Yahoo article: {e}")
                continue

        logger.info(f"Processed {len(filtered_news)} articles from alternative Yahoo method")
        return filtered_news

    def _fetch_yahoo_news_direct(self, symbol, days_back):
        """Fetch Yahoo Finance news using direct API calls"""
        try:
            logger.info(f"Attempting direct Yahoo Finance API call for {symbol}")

            # Yahoo Finance news API endpoint
            url = f"https://query1.finance.yahoo.com/v7/finance/options/{symbol}"

            # Try to get news from the options endpoint which sometimes includes news
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract news if available
            news_items = []
            if 'optionChain' in data and 'result' in data['optionChain']:
                result = data['optionChain']['result'][0] if data['optionChain']['result'] else {}
                if 'news' in result:
                    news_items = result['news']

            if news_items:
                logger.info(f"Found {len(news_items)} news items via direct API")
                return self._process_yahoo_news_data(news_items, symbol, days_back)

            # If no news found, try a different approach - search for news
            logger.info("No news found in options endpoint, trying search approach")
            return self._fetch_yahoo_news_search(symbol, days_back)

        except Exception as e:
            logger.warning(f"Direct Yahoo API call failed: {e}")
            return self._fetch_yahoo_news_search(symbol, days_back)

    def _fetch_yahoo_news_search(self, symbol, days_back):
        """Fetch Yahoo Finance news using search API"""
        try:
            logger.info(f"Attempting Yahoo Finance search API for {symbol}")

            # Yahoo Finance search news endpoint
            search_url = "https://query1.finance.yahoo.com/v1/finance/search"
            params = {
                'q': symbol,
                'quotesCount': 1,
                'newsCount': 10,
                'enableFuzzyQuery': False,
                'quotesQueryId': 'tss_match_phrase_query'
            }

            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            news_items = []
            if 'news' in data:
                news_items = data['news']

            if news_items:
                logger.info(f"Found {len(news_items)} news items via search API")
                return self._process_yahoo_news_data(news_items, symbol, days_back)

            logger.warning("No news found via search API")
            return []

        except Exception as e:
            logger.warning(f"Yahoo Finance search API failed: {e}")
            return []

    def get_newsapi_news(self, symbol, days_back=None):
        """Fetch news articles for a symbol from NewsAPI"""
        if days_back is None:
            days_back = self.news_lookback_days

        newsapi_key = os.getenv("NEWSAPI_KEY")
        if not newsapi_key or newsapi_key == "your_newsapi_key_here":
            logger.warning("NewsAPI key not configured properly")
            return []

        try:
            logger.info(f"Fetching news for {symbol} from NewsAPI (last {days_back} days)")

            # Initialize NewsAPI client
            newsapi = NewsApiClient(api_key=newsapi_key)

            # Calculate date range
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')

            # Search for news about the symbol
            query = f'"{symbol}" OR "{symbol} stock" OR "{symbol} shares"'
            all_articles = newsapi.get_everything(
                q=query,
                from_param=from_date,
                to=to_date,
                language='en',
                sort_by='publishedAt',
                page_size=20
            )

            if not all_articles or all_articles['status'] != 'ok':
                logger.info(f"No news data returned from NewsAPI for {symbol}")
                return []

            logger.info(f"NewsAPI returned {len(all_articles['articles'])} raw articles for {symbol}")

            filtered_news = []
            for article in all_articles['articles']:
                try:
                    # Parse publication date
                    published_str = article.get('publishedAt', '')
                    if published_str:
                        # Remove 'Z' if present and parse
                        published_str = published_str.replace('Z', '+00:00')
                        published_date = datetime.fromisoformat(published_str.replace('T', ' '))
                    else:
                        published_date = datetime.now()

                    # Only include articles with valid titles
                    title = article.get('title', '').strip()
                    if title and len(title) > 10:
                        filtered_news.append({
                            'title': title,
                            'summary': article.get('description', '').strip() if article.get('description') else '',
                            'link': article.get('url', ''),
                            'published': published_date,
                            'publisher': article.get('source', {}).get('name', ''),
                            'symbol': symbol
                        })
                except Exception as e:
                    logger.warning(f"Error processing NewsAPI article: {e}")
                    continue

            logger.info(f"Found {len(filtered_news)} recent news articles for {symbol} from NewsAPI")
            return filtered_news

        except Exception as e:
            logger.error(f"Error fetching news from NewsAPI for {symbol}: {e}")
            return []

    def get_rss_news(self, symbol, days_back=None):
        """Fetch news from major financial RSS feeds"""
        if days_back is None:
            days_back = self.news_lookback_days

        try:
            logger.info(f"Fetching RSS news for {symbol} from financial sources")

            # Major financial news RSS feeds
            rss_feeds = [
                'https://feeds.finance.yahoo.com/rss/2.0/headline',
                'https://www.investing.com/rss/news.rss',
                'https://feeds.marketwatch.com/marketwatch/marketpulse/',
                'https://feeds.bloomberg.com/markets/news.rss',
                'https://feeds.reuters.com/reuters/businessNews',
                'https://feeds.cnbc.com/RSS',
                'https://feeds.wsj.com/wsj/xml/rss/3_7041.xml',  # WSJ Markets
                'https://feeds.foxbusiness.com/foxbusiness/latest'
            ]

            all_news = []
            cutoff_date = datetime.now() - timedelta(days=days_back)

            for feed_url in rss_feeds:
                try:
                    logger.info(f"Fetching from RSS feed: {feed_url}")
                    feed = feedparser.parse(feed_url)

                    if not feed.entries:
                        logger.warning(f"No entries found in RSS feed: {feed_url}")
                        continue

                    for entry in feed.entries:
                        try:
                            # Check if the article is about our symbol
                            title = entry.get('title', '').lower()
                            summary = entry.get('summary', '').lower() if entry.get('summary') else ''

                            # Look for symbol mentions in title or summary
                            symbol_lower = symbol.lower()
                            if symbol_lower not in title and symbol_lower not in summary:
                                continue

                            # Parse publication date
                            published_str = entry.get('published_parsed')
                            if published_str:
                                published_date = datetime(*published_str[:6])
                            else:
                                published_date = datetime.now()

                            # Only include recent articles
                            if published_date >= cutoff_date:
                                all_news.append({
                                    'title': entry.get('title', '').strip(),
                                    'summary': entry.get('summary', '').strip() if entry.get('summary') else '',
                                    'link': entry.get('link', ''),
                                    'published': published_date,
                                    'publisher': entry.get('source', {}).get('title', '') if entry.get('source') else feed.feed.get('title', ''),
                                    'symbol': symbol
                                })

                        except Exception as e:
                            logger.warning(f"Error processing RSS entry: {e}")
                            continue

                    time.sleep(0.5)  # Rate limiting between feeds

                except Exception as e:
                    logger.warning(f"Error fetching RSS feed {feed_url}: {e}")
                    continue

            logger.info(f"Found {len(all_news)} RSS articles for {symbol}")
            return all_news

        except Exception as e:
            logger.error(f"Error fetching RSS news for {symbol}: {e}")
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

        # Try Finnhub as secondary source (if API key is available)
        finnhub_api_key = os.getenv("FINNHUB_API_KEY")
        if finnhub_api_key and finnhub_api_key != "your_finnhub_api_key_here":
            finnhub_news = self.get_finnhub_news(symbol, days_back)
            if finnhub_news:
                all_news.extend(finnhub_news)
                logger.info(f"Added {len(finnhub_news)} articles from Finnhub")
        else:
            logger.info("Finnhub API key not configured, skipping Finnhub news")

        # Try NewsAPI as third source (if API key is available)
        newsapi_key = os.getenv("NEWSAPI_KEY")
        if newsapi_key and newsapi_key != "your_newsapi_key_here":
            newsapi_news = self.get_newsapi_news(symbol, days_back)
            if newsapi_news:
                all_news.extend(newsapi_news)
                logger.info(f"Added {len(newsapi_news)} articles from NewsAPI")
        else:
            logger.info("NewsAPI key not configured, skipping NewsAPI news")

        # Try RSS feeds as fourth source
        rss_news = self.get_rss_news(symbol, days_back)
        if rss_news:
            all_news.extend(rss_news)
            logger.info(f"Added {len(rss_news)} articles from RSS feeds")

        # If no news from any source, try with a longer time period
        if not all_news and days_back <= 3:
            logger.info(f"No recent news found for {symbol}, trying with 7 days...")
            return self.get_combined_news(symbol, days_back=7)

        # Remove duplicates based on title
        seen_titles = set()
        unique_news = []
        for article in all_news:
            title = article['title'].lower().strip()
            if title and title not in seen_titles and len(title) > 10:  # Filter very short titles
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
