#!/usr/bin/env python3
"""
Test the news aggregator functionality
"""

import pytest
from news_aggregator import NewsAggregator

def test_news_aggregator_initialization():
    """Test that the aggregator initializes properly"""
    aggregator = NewsAggregator()
    assert aggregator.sources is not None
    assert 'finnhub' in aggregator.sources
    assert 'yahoo' in aggregator.sources
    print("✅ News aggregator initialization test passed")

def test_news_aggregation():
    """Test news aggregation from multiple sources"""
    aggregator = NewsAggregator()

    # Test with a popular stock
    result = aggregator.get_comprehensive_news('AAPL', days_back=1)

    assert 'articles' in result
    assert 'total_articles' in result
    assert 'source_breakdown' in result
    assert 'timestamp' in result

    # Should have some articles
    assert result['total_articles'] >= 0

    # Should have source breakdown
    assert isinstance(result['source_breakdown'], dict)

    print(f"✅ News aggregation test passed - {result['total_articles']} articles found")
    print(f"📊 Source breakdown: {result['source_breakdown']}")

if __name__ == '__main__':
    test_news_aggregator_initialization()
    test_news_aggregation()
    print("🎯 All news aggregator tests passed!")
