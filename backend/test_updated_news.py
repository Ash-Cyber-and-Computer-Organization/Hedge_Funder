#!/usr/bin/env python3
"""
Test script for the updated news analyzer with enhanced error handling
"""

from news_analyzer import NewsAnalyzer

def test_updated_analyzer():
    """Test the updated news analyzer"""
    print("=== Testing Updated News Analyzer ===")

    analyzer = NewsAnalyzer()

    # Test with a popular stock
    test_symbol = "AAPL"

    print(f"Testing analysis for {test_symbol}...")

    try:
        result = analyzer.analyze_symbol(test_symbol, days_back=3)

        if result:
            print("✅ Analysis successful!")
            print(f"Articles found: {len(result.get('news_articles', []))}")

            if result.get('signal'):
                signal = result['signal']
                sentiment = result['sentiment_data']
                print(f"Signal: {signal['signal']}")
                print(f"Confidence: {signal['confidence']:.3f}")
                print(f"Overall Sentiment: {sentiment['overall_score']:.3f}")
                print(f"Article count: {sentiment['article_count']}")
            else:
                print("No signal generated (insufficient articles)")
        else:
            print("❌ Analysis failed - no result returned")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_updated_analyzer()
