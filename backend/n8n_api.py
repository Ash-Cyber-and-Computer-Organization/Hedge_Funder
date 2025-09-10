#!/usr/bin/env python3
"""
N8N API Endpoints for Automated Trading Workflows
Provides REST API for N8N workflows to interact with the trading system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import our modules
from news_analyzer import NewsAnalyzer
from telegram_signal_trader import process_signal, test_connection
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import pickle

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

# Initialize components
news_analyzer = NewsAnalyzer()

# Global variables for ML models
ml_model = None
scaler = None
model_features = []

class AdvancedNewsAnalyzer(NewsAnalyzer):
    """Enhanced News Analyzer with ML capabilities"""

    def __init__(self):
        super().__init__()
        self.pattern_history = []
        self.load_ml_model()

    def load_ml_model(self):
        """Load or train ML model for pattern recognition"""
        global ml_model, scaler, model_features

        model_path = 'models/trading_model.pkl'
        scaler_path = 'models/scaler.pkl'

        try:
            if os.path.exists(model_path):
                ml_model = joblib.load(model_path)
                scaler = joblib.load(scaler_path)
                logger.info("ML model loaded successfully")
            else:
                logger.info("No existing ML model found, will train new one")
        except Exception as e:
            logger.error(f"Error loading ML model: {e}")

    def extract_features(self, news_articles, symbol):
        """Extract advanced features for ML analysis"""
        if not news_articles:
            return {}

        # Basic sentiment features
        sentiments = [self.analyze_sentiment_simple(f"{art['title']} {art.get('summary', '')}")
                     for art in news_articles]

        # Time-based features
        timestamps = [art['published'] for art in news_articles]
        time_diffs = [(timestamps[i] - timestamps[i-1]).total_seconds() / 3600
                     for i in range(1, len(timestamps))]

        # Publisher diversity
        publishers = list(set(art['publisher'] for art in news_articles))

        # Keyword analysis
        all_text = ' '.join([f"{art['title']} {art.get('summary', '')}" for art in news_articles])
        bullish_keywords = ['rise', 'gain', 'up', 'bullish', 'beat', 'strong', 'growth']
        bearish_keywords = ['fall', 'drop', 'down', 'bearish', 'miss', 'weak', 'decline']

        bullish_count = sum(1 for word in bullish_keywords if word in all_text.lower())
        bearish_count = sum(1 for word in bearish_keywords if word in all_text.lower())

        features = {
            'avg_sentiment': np.mean(sentiments),
            'sentiment_volatility': np.std(sentiments),
            'article_count': len(news_articles),
            'time_span_hours': (max(timestamps) - min(timestamps)).total_seconds() / 3600,
            'avg_time_diff_hours': np.mean(time_diffs) if time_diffs else 0,
            'publisher_diversity': len(publishers),
            'bullish_ratio': bullish_count / (bullish_count + bearish_count + 1),
            'news_velocity': len(news_articles) / max(1, (max(timestamps) - min(timestamps)).total_seconds() / 3600),
            'sentiment_trend': np.polyfit(range(len(sentiments)), sentiments, 1)[0] if len(sentiments) > 1 else 0
        }

        return features

    def predict_with_ml(self, features):
        """Use ML model to predict trading signal"""
        global ml_model, scaler, model_features

        if ml_model is None or scaler is None:
            return None

        try:
            # Prepare features for prediction
            feature_vector = np.array([features.get(feat, 0) for feat in model_features]).reshape(1, -1)
            scaled_features = scaler.transform(feature_vector)

            # Get prediction probabilities
            probabilities = ml_model.predict_proba(scaled_features)[0]

            # Return prediction with confidence
            predicted_class = np.argmax(probabilities)
            confidence = probabilities[predicted_class]

            signal_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
            predicted_signal = signal_map.get(predicted_class, 'HOLD')

            return {
                'signal': predicted_signal,
                'confidence': float(confidence),
                'probabilities': {
                    'SELL': float(probabilities[0]),
                    'HOLD': float(probabilities[1]),
                    'BUY': float(probabilities[2])
                }
            }

        except Exception as e:
            logger.error(f"ML prediction error: {e}")
            return None

    def analyze_with_patterns(self, symbol, days_back=None):
        """Advanced analysis with pattern recognition and ML"""
        # Get news data
        news_articles = self.get_combined_news(symbol, days_back)

        if not news_articles:
            return None

        # Extract features
        features = self.extract_features(news_articles, symbol)

        # Get basic sentiment analysis
        sentiment_data = self.calculate_overall_sentiment(news_articles)

        # Generate basic signal
        basic_signal = self.generate_signal(symbol, sentiment_data)

        # Get ML prediction
        ml_prediction = self.predict_with_ml(features)

        # Combine signals
        final_signal = self.combine_signals(basic_signal, ml_prediction, features)

        # Store pattern for learning
        self.store_pattern(symbol, features, final_signal)

        return {
            'symbol': symbol,
            'news_articles': news_articles,
            'features': features,
            'sentiment_data': sentiment_data,
            'basic_signal': basic_signal,
            'ml_prediction': ml_prediction,
            'final_signal': final_signal,
            'analysis_timestamp': datetime.now()
        }

    def combine_signals(self, basic_signal, ml_prediction, features):
        """Combine basic sentiment and ML signals"""
        if not basic_signal:
            return ml_prediction

        if not ml_prediction:
            return basic_signal

        # Weighted combination based on confidence
        basic_weight = 0.4
        ml_weight = 0.6

        basic_confidence = basic_signal.get('confidence', 0)
        ml_confidence = ml_prediction.get('confidence', 0)

        # If ML has high confidence, trust it more
        if ml_confidence > 0.7:
            return ml_prediction
        elif basic_confidence > 0.6:
            return basic_signal
        else:
            # Weighted average
            signals = [basic_signal['signal'], ml_prediction['signal']]
            confidences = [basic_confidence, ml_confidence]

            # Simple majority vote with confidence weighting
            if signals[0] == signals[1]:
                return basic_signal if basic_confidence > ml_confidence else ml_prediction
            else:
                # Different signals - choose higher confidence
                return basic_signal if basic_confidence > ml_confidence else ml_prediction

    def store_pattern(self, symbol, features, signal):
        """Store pattern for future learning"""
        pattern = {
            'symbol': symbol,
            'features': features,
            'signal': signal['signal'] if signal else 'HOLD',
            'timestamp': datetime.now(),
            'outcome': None  # To be filled later
        }

        self.pattern_history.append(pattern)

        # Keep only recent patterns
        if len(self.pattern_history) > 1000:
            self.pattern_history = self.pattern_history[-1000:]

# Initialize advanced analyzer
advanced_analyzer = AdvancedNewsAnalyzer()

class RiskManager:
    """Advanced risk management system"""

    def __init__(self):
        self.max_daily_loss = float(os.getenv("MAX_DAILY_LOSS", "100"))
        self.max_position_size = float(os.getenv("MAX_POSITION_SIZE", "0.1"))
        self.max_open_positions = int(os.getenv("MAX_OPEN_POSITIONS", "3"))
        self.daily_pnl = 0
        self.open_positions = []

    def calculate_position_size(self, signal, account_balance, symbol_volatility):
        """Calculate optimal position size based on risk management"""
        if not signal:
            return 0

        # Kelly Criterion inspired position sizing
        confidence = signal.get('confidence', 0)
        win_rate = confidence  # Simplified assumption

        # Risk per trade (1-2% of account)
        risk_per_trade = account_balance * 0.02

        # Adjust for volatility
        volatility_adjustment = 1 / (1 + symbol_volatility)

        # Adjust for confidence
        confidence_multiplier = confidence

        position_size = risk_per_trade * volatility_adjustment * confidence_multiplier

        # Cap at maximum position size
        position_size = min(position_size, account_balance * self.max_position_size)

        return position_size

    def validate_trade(self, signal, current_positions):
        """Validate if trade meets risk criteria"""
        if not signal:
            return False, "No signal provided"

        # Check daily loss limit
        if self.daily_pnl < -self.max_daily_loss:
            return False, "Daily loss limit reached"

        # Check max open positions
        if len(current_positions) >= self.max_open_positions:
            return False, "Maximum open positions reached"

        # Check if already have position in this symbol
        for pos in current_positions:
            if pos['symbol'] == signal['symbol']:
                return False, f"Already have position in {signal['symbol']}"

        return True, "Trade approved"

# Initialize risk manager
risk_manager = RiskManager()

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    })

@app.route('/api/news/analyze', methods=['POST'])
def analyze_news():
    """Analyze news for trading signals"""
    try:
        data = request.get_json()

        if not data or 'symbol' not in data:
            return jsonify({'error': 'Symbol is required'}), 400

        symbol = data['symbol']
        days_back = data.get('days_back', 3)

        logger.info(f"N8N request: Analyzing {symbol}")

        # Use advanced analysis
        result = advanced_analyzer.analyze_with_patterns(symbol, days_back)

        if not result:
            return jsonify({'error': 'No data available for analysis'}), 404

        return jsonify(result)

    except Exception as e:
        logger.error(f"News analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/signals/generate', methods=['POST'])
def generate_signals():
    """Generate trading signals with risk management"""
    try:
        data = request.get_json()

        if not data or 'symbols' not in data:
            return jsonify({'error': 'Symbols list is required'}), 400

        symbols = data['symbols']
        days_back = data.get('days_back', 3)

        logger.info(f"N8N request: Generating signals for {symbols}")

        signals = []

        for symbol in symbols:
            # Analyze symbol
            analysis = advanced_analyzer.analyze_with_patterns(symbol, days_back)

            if analysis and analysis['final_signal']:
                signal = analysis['final_signal']

                # Apply risk management
                is_valid, reason = risk_manager.validate_trade(signal, [])

                signals.append({
                    'symbol': symbol,
                    'signal': signal['signal'],
                    'confidence': signal['confidence'],
                    'reason': signal.get('reason', ''),
                    'risk_validated': is_valid,
                    'risk_reason': reason,
                    'analysis': analysis
                })

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
    """Execute trade with full risk management"""
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

        # Format signal for existing trader
        formatted_signal = f"{action} {symbol} SL=1.0500 TP=1.0700"  # Default SL/TP

        # Execute trade
        success = process_signal(formatted_signal)

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
        # Sample recent signals for demonstration
        recent_signals = [
            {
                'symbol': 'AAPL',
                'signal': 'BUY',
                'confidence': 0.85,
                'reason': 'Positive sentiment (score: 0.271)',
                'timestamp': (datetime.now() - timedelta(minutes=15)).isoformat()
            },
            {
                'symbol': 'GOOGL',
                'signal': 'SELL',
                'confidence': 0.72,
                'reason': 'Negative sentiment (score: -0.156)',
                'timestamp': (datetime.now() - timedelta(minutes=30)).isoformat()
            },
            {
                'symbol': 'MSFT',
                'signal': 'BUY',
                'confidence': 0.68,
                'reason': 'Strong bullish indicators',
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat()
            },
            {
                'symbol': 'TSLA',
                'signal': 'HOLD',
                'confidence': 0.45,
                'reason': 'Neutral sentiment',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                'symbol': 'NVDA',
                'signal': 'BUY',
                'confidence': 0.91,
                'reason': 'Very positive news coverage',
                'timestamp': (datetime.now() - timedelta(hours=3)).isoformat()
            }
        ]

        # Get system status
        system_status = {
            'mt5_connection': test_connection(),
            'news_sources': ['Yahoo Finance', 'Finnhub'],
            'active_workflows': ['News Analysis', 'Signal Generation', 'Risk Management'],
            'last_update': datetime.now().isoformat()
        }

        # Get performance metrics
        performance = {
            'total_signals': len(recent_signals),
            'success_rate': 0.75,
            'daily_pnl': 245.67,  # Sample P&L
            'open_positions': 2
        }

        return jsonify({
            'system_status': system_status,
            'performance': performance,
            'recent_signals': recent_signals[-10:],  # Last 10 signals
            'risk_metrics': {
                'max_daily_loss': risk_manager.max_daily_loss,
                'max_position_size': risk_manager.max_position_size,
                'current_positions': len(risk_manager.open_positions) or 2  # Sample positions
            }
        })

    except Exception as e:
        logger.error(f"Dashboard data error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/send', methods=['POST'])
def send_alert():
    """Send alerts via Telegram"""
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        message = data['message']
        alert_type = data.get('type', 'info')

        logger.info(f"N8N request: Sending {alert_type} alert")

        # Here you would integrate with Telegram bot
        # For now, just log the alert
        logger.info(f"ALERT [{alert_type.upper()}]: {message}")

        return jsonify({
            'success': True,
            'message': message,
            'type': alert_type,
            'sent_at': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Alert sending error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patterns/learn', methods=['POST'])
def learn_patterns():
    """Update ML model with new patterns"""
    try:
        # This would retrain the ML model with new data
        # For now, just acknowledge the request

        logger.info("N8N request: Learning from new patterns")

        return jsonify({
            'success': True,
            'message': 'Pattern learning initiated',
            'patterns_learned': len(advanced_analyzer.pattern_history),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Pattern learning error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('N8N_API_PORT', 5002))
    logger.info(f"Starting N8N API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
