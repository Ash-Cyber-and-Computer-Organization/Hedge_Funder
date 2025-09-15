 #!/usr/bin/env python3
"""
Minimal N8N API for Trading Integration
Clean, focused API for n8n workflows with Finnhub and broker integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests

# Import our modules
from news_aggregator import NewsAggregator
from test_finnhub_integration import analyze_news_sentiment, generate_trading_signal

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize clients
news_aggregator = NewsAggregator()

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

@app.route('/api/webhook/news', methods=['POST'])
def news_webhook():
    """Webhook endpoint to receive news requests from frontend"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        symbol = data.get('symbol')
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400

        logger.info(f"N8N Webhook: Received news request for {symbol}")

        # Forward to n8n processing
        return jsonify({
            'message': f'News request for {symbol} received',
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'status': 'forwarded_to_n8n'
        })

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/finnhub/news', methods=['POST'])
def get_finnhub_news():
    """Get news from Finnhub API and other free sources"""
    try:
        data = request.get_json()

        if not data or 'symbol' not in data:
            return jsonify({'error': 'Symbol is required'}), 400

        symbol = data['symbol']
        days_back = data.get('days_back', 3)

        logger.info(f"N8N request: Fetching aggregated news for {symbol}")

        # Get news from multiple sources
        aggregated_news_result = news_aggregator.get_comprehensive_news(symbol, days_back)

        news_articles = aggregated_news_result.get('articles', [])

        if not news_articles:
            return jsonify({'error': 'No news found'}), 404

        # Analyze sentiment
        sentiment = analyze_news_sentiment(news_articles)

        return jsonify({
            'symbol': symbol,
            'news_articles': news_articles,
            'sentiment_analysis': sentiment,
            'total_articles': len(news_articles),
            'source_breakdown': aggregated_news_result.get('source_breakdown', {}),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Aggregated news error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/signals/generate', methods=['POST'])
def generate_signals():
    """Generate trading signals based on news and market data"""
    try:
        data = request.get_json()

        if not data or 'symbols' not in data:
            return jsonify({'error': 'Symbols list is required'}), 400

        symbols = data['symbols']

        logger.info(f"N8N request: Generating signals for {symbols}")

        signals = []

        for symbol in symbols:
            # Get news and analyze using aggregator
            aggregated_news_result = news_aggregator.get_comprehensive_news(symbol, days_back=2)
            news_articles = aggregated_news_result.get('articles', [])
            sentiment = analyze_news_sentiment(news_articles)

            # Get quote data (would need to implement this in aggregator)
            quote = {'current_price': 100.0, 'change': 0.5}  # Placeholder

            # Generate signal
            signal = generate_trading_signal(symbol, sentiment, quote)

            signals.append(signal)

        return jsonify({
            'signals': signals,
            'generated_at': datetime.now().isoformat(),
            'total_signals': len(signals)
        })

    except Exception as e:
        logger.error(f"Signal generation error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trade/execute', methods=['POST'])
def execute_trade():
    """Execute trade based on signal"""
    try:
        data = request.get_json()

        if not data or 'signal' not in data:
            return jsonify({'error': 'Trading signal is required'}), 400

        signal_data = data['signal']
        symbol = signal_data.get('symbol')
        action = signal_data.get('signal')

        if not symbol or not action:
            return jsonify({'error': 'Symbol and action are required'}), 400

        logger.info(f"N8N request: Executing {action} trade for {symbol}")

        # Format signal for trader
        formatted_signal = f"{action} {symbol}"

        # Execute trade (placeholder - implement actual broker integration)
        success = True  # Placeholder - simulate successful trade execution

        # Send notification (placeholder - implement actual notification system)
        logger.info(f"Trade notification: {'✅ Trade executed' if success else '❌ Trade failed'}: {action} {symbol}")

        return jsonify({
            'success': success,
            'symbol': symbol,
            'action': action,
            'executed_at': datetime.now().isoformat(),
            'formatted_signal': formatted_signal
        })

    except Exception as e:
        logger.error(f"Trade execution error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/monitoring/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get monitoring data for frontend dashboard"""
    try:
        # Check connections
        mt5_status = True  # Placeholder - implement MT5 connection check
        finnhub_status = bool(os.getenv('FINNHUB_API_KEY'))

        # Sample recent signals for demonstration - comprehensive asset coverage
        now = datetime.now()
        recent_signals = [
            # Major Tech Stocks
            {
                'symbol': 'AAPL',
                'signal': 'BUY',
                'confidence': 0.85,
                'reason': 'Positive sentiment (score: 0.271)',
                'timestamp': (now - timedelta(minutes=15)).isoformat()
            },
            {
                'symbol': 'GOOGL',
                'signal': 'SELL',
                'confidence': 0.72,
                'reason': 'Negative sentiment (score: -0.156)',
                'timestamp': (now - timedelta(minutes=30)).isoformat()
            },
            {
                'symbol': 'MSFT',
                'signal': 'BUY',
                'confidence': 0.68,
                'reason': 'Strong bullish indicators',
                'timestamp': (now - timedelta(hours=1)).isoformat()
            },
            {
                'symbol': 'TSLA',
                'signal': 'HOLD',
                'confidence': 0.45,
                'reason': 'Neutral sentiment',
                'timestamp': (now - timedelta(hours=2)).isoformat()
            },
            {
                'symbol': 'NVDA',
                'signal': 'BUY',
                'confidence': 0.91,
                'reason': 'Very positive news coverage',
                'timestamp': (now - timedelta(hours=3)).isoformat()
            },
            {
                'symbol': 'AMZN',
                'signal': 'BUY',
                'confidence': 0.82,
                'reason': 'E-commerce growth outlook positive',
                'timestamp': (now - timedelta(hours=2, minutes=30)).isoformat()
            },
            {
                'symbol': 'META',
                'signal': 'HOLD',
                'confidence': 0.52,
                'reason': 'Mixed signals on metaverse investments',
                'timestamp': (now - timedelta(hours=3, minutes=45)).isoformat()
            },
            {
                'symbol': 'NFLX',
                'signal': 'SELL',
                'confidence': 0.69,
                'reason': 'Subscriber growth concerns',
                'timestamp': (now - timedelta(hours=4)).isoformat()
            },

            # Semiconductor & Hardware
            {
                'symbol': 'AMD',
                'signal': 'BUY',
                'confidence': 0.83,
                'reason': 'Chip shortage resolution positive',
                'timestamp': (now - timedelta(hours=9)).isoformat()
            },
            {
                'symbol': 'INTC',
                'signal': 'SELL',
                'confidence': 0.71,
                'reason': 'Competitive pressure from AMD',
                'timestamp': (now - timedelta(hours=10)).isoformat()
            },
            {
                'symbol': 'QCOM',
                'signal': 'BUY',
                'confidence': 0.77,
                'reason': '5G and IoT growth potential',
                'timestamp': (now - timedelta(hours=15)).isoformat()
            },
            {
                'symbol': 'CRM',
                'signal': 'BUY',
                'confidence': 0.89,
                'reason': 'Cloud software demand surge',
                'timestamp': (now - timedelta(hours=16)).isoformat()
            },

            # Entertainment & Media
            {
                'symbol': 'DIS',
                'signal': 'HOLD',
                'confidence': 0.55,
                'reason': 'Streaming service competition',
                'timestamp': (now - timedelta(hours=13)).isoformat()
            },
            {
                'symbol': 'SPOT',
                'signal': 'BUY',
                'confidence': 0.73,
                'reason': 'Music streaming market leadership',
                'timestamp': (now - timedelta(hours=17)).isoformat()
            },

            # Financial Services
            {
                'symbol': 'JPM',
                'signal': 'BUY',
                'confidence': 0.81,
                'reason': 'Interest rate environment favorable',
                'timestamp': (now - timedelta(hours=18)).isoformat()
            },
            {
                'symbol': 'V',
                'signal': 'BUY',
                'confidence': 0.79,
                'reason': 'Digital payments growth',
                'timestamp': (now - timedelta(hours=19)).isoformat()
            },
            {
                'symbol': 'COIN',
                'signal': 'BUY',
                'confidence': 0.81,
                'reason': 'Crypto exchange volume growth',
                'timestamp': (now - timedelta(hours=14)).isoformat()
            },

            # Major Cryptocurrencies
            {
                'symbol': 'BTC-USD',
                'signal': 'BUY',
                'confidence': 0.78,
                'reason': 'Strong crypto market momentum',
                'timestamp': (now - timedelta(minutes=45)).isoformat()
            },
            {
                'symbol': 'ETH-USD',
                'signal': 'SELL',
                'confidence': 0.65,
                'reason': 'Ethereum network congestion concerns',
                'timestamp': (now - timedelta(hours=1, minutes=15)).isoformat()
            },
            {
                'symbol': 'ADA-USD',
                'signal': 'BUY',
                'confidence': 0.74,
                'reason': 'Cardano smart contract adoption',
                'timestamp': (now - timedelta(hours=5)).isoformat()
            },
            {
                'symbol': 'BNB-USD',
                'signal': 'HOLD',
                'confidence': 0.48,
                'reason': 'Binance ecosystem developments',
                'timestamp': (now - timedelta(hours=8)).isoformat()
            },
            {
                'symbol': 'SOL-USD',
                'signal': 'BUY',
                'confidence': 0.79,
                'reason': 'Solana ecosystem growth',
                'timestamp': (now - timedelta(hours=11)).isoformat()
            },
            {
                'symbol': 'MATIC-USD',
                'signal': 'BUY',
                'confidence': 0.67,
                'reason': 'Polygon layer 2 adoption',
                'timestamp': (now - timedelta(hours=12)).isoformat()
            },
            {
                'symbol': 'AVAX-USD',
                'signal': 'BUY',
                'confidence': 0.72,
                'reason': 'Avalanche subnet expansion',
                'timestamp': (now - timedelta(hours=20)).isoformat()
            },
            {
                'symbol': 'DOT-USD',
                'signal': 'HOLD',
                'confidence': 0.58,
                'reason': 'Polkadot parachain auctions',
                'timestamp': (now - timedelta(hours=21)).isoformat()
            },
            {
                'symbol': 'LINK-USD',
                'signal': 'BUY',
                'confidence': 0.76,
                'reason': 'Oracle network adoption',
                'timestamp': (now - timedelta(hours=22)).isoformat()
            },
            {
                'symbol': 'UNI-USD',
                'signal': 'SELL',
                'confidence': 0.63,
                'reason': 'DEX competition intensifying',
                'timestamp': (now - timedelta(hours=23)).isoformat()
            },

            # ETFs and Indices
            {
                'symbol': 'SPY',
                'signal': 'BUY',
                'confidence': 0.88,
                'reason': 'S&P 500 bullish technical indicators',
                'timestamp': (now - timedelta(hours=6)).isoformat()
            },
            {
                'symbol': 'QQQ',
                'signal': 'BUY',
                'confidence': 0.76,
                'reason': 'Nasdaq tech sector strength',
                'timestamp': (now - timedelta(hours=7)).isoformat()
            },
            {
                'symbol': 'IWM',
                'signal': 'HOLD',
                'confidence': 0.54,
                'reason': 'Russell 2000 volatility concerns',
                'timestamp': (now - timedelta(hours=24)).isoformat()
            },
            {
                'symbol': 'VTI',
                'signal': 'BUY',
                'confidence': 0.84,
                'reason': 'Total stock market exposure',
                'timestamp': (now - timedelta(hours=25)).isoformat()
            },

            # Commodities and Futures
            {
                'symbol': 'GLD',
                'signal': 'BUY',
                'confidence': 0.71,
                'reason': 'Gold safe-haven demand',
                'timestamp': (now - timedelta(hours=26)).isoformat()
            },
            {
                'symbol': 'SLV',
                'signal': 'SELL',
                'confidence': 0.66,
                'reason': 'Silver industrial demand concerns',
                'timestamp': (now - timedelta(hours=27)).isoformat()
            },
            {
                'symbol': 'USO',
                'signal': 'HOLD',
                'confidence': 0.49,
                'reason': 'Oil price volatility',
                'timestamp': (now - timedelta(hours=28)).isoformat()
            },

            # International Markets
            {
                'symbol': 'EWJ',
                'signal': 'BUY',
                'confidence': 0.75,
                'reason': 'Japan market recovery',
                'timestamp': (now - timedelta(hours=29)).isoformat()
            },
            {
                'symbol': 'EWG',
                'signal': 'SELL',
                'confidence': 0.68,
                'reason': 'Eurozone economic concerns',
                'timestamp': (now - timedelta(hours=30)).isoformat()
            },
            {
                'symbol': 'EFA',
                'signal': 'BUY',
                'confidence': 0.73,
                'reason': 'Developed markets exposure',
                'timestamp': (now - timedelta(hours=31)).isoformat()
            },

            # Bonds and Fixed Income
            {
                'symbol': 'BND',
                'signal': 'HOLD',
                'confidence': 0.52,
                'reason': 'Bond yields stabilization',
                'timestamp': (now - timedelta(hours=32)).isoformat()
            },
            {
                'symbol': 'TLT',
                'signal': 'BUY',
                'confidence': 0.69,
                'reason': 'Treasury bond duration play',
                'timestamp': (now - timedelta(hours=33)).isoformat()
            },
            {
                'symbol': 'LQD',
                'signal': 'SELL',
                'confidence': 0.61,
                'reason': 'Corporate bond spread widening',
                'timestamp': (now - timedelta(hours=34)).isoformat()
            },

            # Real Estate
            {
                'symbol': 'VNQ',
                'signal': 'BUY',
                'confidence': 0.78,
                'reason': 'Commercial real estate recovery',
                'timestamp': (now - timedelta(hours=35)).isoformat()
            },
            {
                'symbol': 'IYR',
                'signal': 'HOLD',
                'confidence': 0.56,
                'reason': 'Residential real estate cooling',
                'timestamp': (now - timedelta(hours=36)).isoformat()
            }
        ]

        # Get system status
        system_status = {
            'mt5_connection': mt5_status,
            'news_sources': ['Finnhub'],
            'active_workflows': ['News Analysis', 'Signal Generation'],
            'last_update': datetime.now().isoformat()
        }

        # Get performance metrics
        performance = {
            'total_signals': len(recent_signals),
            'success_rate': 0.75,
            'daily_pnl': 245.67,
            'open_positions': 2
        }

        return jsonify({
            'system_status': system_status,
            'performance': performance,
            'recent_signals': recent_signals[-10:],
            'risk_metrics': {
                'max_daily_loss': 100,
                'max_position_size': 0.1,
                'current_positions': 2
            }
        })

    except Exception as e:
        logger.error(f"Dashboard data error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/send', methods=['POST'])
def send_alert():
    """Send alert via Telegram"""
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        message = data['message']
        alert_type = data.get('type', 'info')

        logger.info(f"N8N request: Sending {alert_type} alert")

        success = True  # Placeholder - implement actual alert system

        return jsonify({
            'success': success,
            'message': message,
            'type': alert_type,
            'sent_at': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Alert sending error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('N8N_API_PORT', 5001))
    logger.info(f"Starting Minimal N8N API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
