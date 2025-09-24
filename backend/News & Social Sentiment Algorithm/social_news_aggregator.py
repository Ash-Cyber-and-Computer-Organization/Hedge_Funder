#!/usr/bin/env python3
"""
Social Media News Aggregator
Collects news and discussions from Reddit and Twitter for trading insights
"""

import os
import logging
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SocialNewsAggregator:
    """Aggregates news from Reddit and Twitter for trading insights"""

    def __init__(self):
        self.sources = {
            'reddit': RedditNewsClient(),
            'twitter': TwitterNewsClient()
        }

    def get_social_news(self, symbol, days_back=3):
        """Get news from Reddit and Twitter"""
        all_news = []
        source_stats = {}

        for source_name, client in self.sources.items():
            try:
                logger.info(f"Fetching social news from {source_name} for {symbol}")
                news = client.get_news(symbol, days_back)
                all_news.extend(news)
                source_stats[source_name] = len(news)
                logger.info(f"✅ {source_name}: {len(news)} posts/tweets")

                # Rate limiting
                time.sleep(1)

            except Exception as e:
                logger.warning(f"❌ {source_name} failed: {e}")
                source_stats[source_name] = 0

        # Remove duplicates based on title/content similarity
        unique_news = self._remove_duplicates(all_news)

        logger.info(f"📊 Total social posts: {len(all_news)} → {len(unique_news)} unique")

        return {
            'articles': unique_news,
            'total_articles': len(unique_news),
            'source_breakdown': source_stats,
            'timestamp': datetime.now().isoformat()
        }

    def _remove_duplicates(self, articles):
        """Remove duplicate articles based on content similarity"""
        if not articles:
            return []

        unique_articles = []

        for article in articles:
            content = article.get('title', '').lower().strip() + ' ' + article.get('summary', '').lower().strip()

            # Check if similar content already exists
            is_duplicate = False
            for existing in unique_articles:
                existing_content = existing.get('title', '').lower().strip() + ' ' + existing.get('summary', '').lower().strip()

                # Simple similarity check (70% overlap)
                if self._content_similarity(content, existing_content) > 0.7:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_articles.append(article)

        return unique_articles

    def _content_similarity(self, content1, content2):
        """Calculate content similarity using word overlap"""
        words1 = set(content1.split())
        words2 = set(content2.split())

        if not words1 or not words2:
            return 0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0

class RedditNewsClient:
    """Reddit API Client using PRAW"""

    def __init__(self):
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'HedgeFunder/1.0')
        self.reddit = None

        if self.client_id and self.client_secret:
            try:
                import praw
                self.reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    user_agent=self.user_agent
                )
            except ImportError:
                logger.warning("PRAW not installed. Install with: pip install praw")

    def get_news(self, symbol, days_back=3):
        if not self.reddit:
            return []

        try:
            # Search in relevant subreddits
            subreddits = ['wallstreetbets', 'stocks', 'investing', 'StockMarket']
            all_posts = []

            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)

                    # Search for posts containing the symbol
                    query = f'"{symbol}"'
                    posts = subreddit.search(query, sort='new', time_filter='week', limit=10)

                    for post in posts:
                        # Check if post is within days_back
                        post_date = datetime.fromtimestamp(post.created_utc)
                        if post_date >= datetime.now() - timedelta(days=days_back):
                            all_posts.append({
                                'title': post.title,
                                'summary': post.selftext[:500] if post.selftext else '',
                                'source': f'Reddit/{subreddit_name}',
                                'url': f'https://reddit.com{post.permalink}',
                                'published': post_date.isoformat(),
                                'symbol': symbol,
                                'api_source': 'reddit',
                                'score': post.score,
                                'comments': post.num_comments
                            })

                except Exception as e:
                    logger.warning(f"Reddit subreddit {subreddit_name} error: {e}")

            return all_posts

        except Exception as e:
            logger.error(f"Reddit error: {e}")
            return []

class TwitterNewsClient:
    """Twitter API Client using Tweepy"""

    def __init__(self):
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.client = None

        if self.bearer_token:
            try:
                import tweepy
                self.client = tweepy.Client(bearer_token=self.bearer_token)
            except ImportError:
                logger.warning("Tweepy not installed. Install with: pip install tweepy")

    def get_news(self, symbol, days_back=3):
        if not self.client:
            return []

        try:
            # Search for tweets containing the symbol
            query = f'"{symbol}" stock OR "{symbol}" shares OR "{symbol}" market -is:retweet lang:en'
            start_time = (datetime.now() - timedelta(days=days_back)).isoformat() + 'Z'

            tweets = self.client.search_recent_tweets(
                query=query,
                start_time=start_time,
                max_results=20,
                tweet_fields=['created_at', 'public_metrics', 'author_id']
            )

            if not tweets.data:
                return []

            articles = []
            for tweet in tweets.data:
                articles.append({
                    'title': tweet.text[:100] + '...' if len(tweet.text) > 100 else tweet.text,
                    'summary': tweet.text,
                    'source': 'Twitter',
                    'url': f'https://twitter.com/i/web/status/{tweet.id}',
                    'published': tweet.created_at.isoformat(),
                    'symbol': symbol,
                    'api_source': 'twitter',
                    'likes': tweet.public_metrics.get('like_count', 0),
                    'retweets': tweet.public_metrics.get('retweet_count', 0)
                })

            return articles

        except Exception as e:
            logger.error(f"Twitter error: {e}")
            return []

def test_social_news_aggregator():
    """Test the social news aggregator"""
    aggregator = SocialNewsAggregator()

    print("📰 Testing Social Media News Aggregator...")

    # Test with popular stocks
    test_symbols = ['AAPL', 'TSLA', 'GOOGL']

    for symbol in test_symbols:
        print(f"\n📊 Testing {symbol}...")

        try:
            result = aggregator.get_social_news(symbol, days_back=2)

            print(f"✅ {symbol}: {result['total_articles']} unique posts/tweets")
            print(f"📈 Source breakdown: {result['source_breakdown']}")

            if result['articles']:
                print(f"📝 Sample: {result['articles'][0]['title'][:60]}...")
                print(f"🔗 Source: {result['articles'][0]['api_source']}")

        except Exception as e:
            print(f"❌ {symbol} failed: {e}")

        time.sleep(2)  # Rate limiting

    print("\n🎯 Social news aggregator test completed!")

if __name__ == '__main__':
    test_social_news_aggregator()
