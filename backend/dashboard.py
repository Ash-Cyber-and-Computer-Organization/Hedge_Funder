from flask import Flask, render_template, jsonify
from data_storage import get_data_storage, init_data_storage
import os

app = Flask(__name__, template_folder='templates')

# Initialize data storage
storage = init_data_storage()

@app.route('/')
def index():
    """Serve the dashboard HTML"""
    return render_template('dashboard.html')

@app.route('/api/dashboard')
def get_dashboard_data():
    """Get dashboard data"""
    try:
        dashboard_data = storage.get_dashboard_data()
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/signals')
def get_trade_signals():
    """Get recent trade signals"""
    try:
        signals = storage.get_trade_signals()
        return jsonify(signals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio')
def get_portfolio():
    """Get portfolio positions"""
    try:
        portfolio = storage.get_portfolio()
        return jsonify(portfolio)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions')
def get_transactions():
    """Get transaction history"""
    try:
        transactions = storage.get_transactions()
        return jsonify(transactions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get database statistics"""
    try:
        stats = storage.get_database_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
