# 🚀 Advanced N8N Trading Integration Setup

## 📋 Overview

This setup provides a complete automated trading system using N8N workflows, advanced news analysis with AI/ML capabilities, risk management, and real-time monitoring.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   N8N Workflows │───▶│   N8N API       │───▶│   Trading Bot   │
│                 │    │   (Flask)       │    │   (MT5)         │
│ • News Analysis │    │ • REST Endpoints│    │ • Signal Exec   │
│ • Risk Monitor  │    │ • ML Models     │    │ • Risk Mgmt     │
│ • Market Sent.  │    │ • Telegram API  │    │ • P&L Tracking  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Frontend      │
                       │   Dashboard     │
                       │ • Real-time     │
                       │ • Charts        │
                       │ • Controls      │
                       └─────────────────┘
```

## ⚡ Quick Start

### 1. Install Dependencies

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend
npm install

# N8N (global installation)
npm install n8n -g
```

### 2. Configure Environment

Create `.env` file in backend directory:

```env
# MT5 Configuration
MT5_LOGIN=your_login
MT5_PASSWORD=your_password
MT5_SERVER=your_server

# News API Keys
FINNHUB_API_KEY=your_finnhub_key

# Telegram Bot (for alerts)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Risk Management
MAX_DAILY_LOSS=100
MAX_POSITION_SIZE=0.1
MAX_OPEN_POSITIONS=3

# News Analysis
SENTIMENT_THRESHOLD=0.1
NEWS_LOOKBACK_DAYS=7
MIN_NEWS_ARTICLES=3
```

### 3. Start Services

```bash
# Terminal 1: Start N8N API Server
cd backend
python n8n_api.py

# Terminal 2: Start N8N Workflow Engine
n8n start

# Terminal 3: Start Frontend Dashboard
cd frontend
npm run dev
```

## 🤖 N8N Workflows

### 1. News Analysis Workflow
- **Schedule**: Every 15 minutes
- **Function**: Fetches news, analyzes sentiment, generates signals
- **Output**: Trading signals with confidence scores

### 2. Risk Monitoring Workflow
- **Schedule**: Every 5 minutes
- **Function**: Monitors P&L, position limits, connection status
- **Output**: Risk alerts via Telegram

### 3. Market Sentiment Workflow
- **Schedule**: Every 2 hours
- **Function**: Analyzes overall market sentiment from major indices
- **Output**: Market mood updates and recommendations

### 4. Pattern Learning Workflow
- **Schedule**: Weekly (Mondays)
- **Function**: Updates ML model with new trading patterns
- **Output**: Improved prediction accuracy

## 📊 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/news/analyze` | Analyze news for symbol |
| POST | `/api/signals/generate` | Generate trading signals |
| POST | `/api/trade/execute` | Execute trade |
| GET | `/api/monitoring/dashboard` | Get dashboard data |
| POST | `/api/alerts/send` | Send Telegram alert |
| POST | `/api/patterns/learn` | Trigger ML learning |

### Example API Calls

```bash
# Analyze news for AAPL
curl -X POST http://localhost:5001/api/news/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "days_back": 3}'

# Generate signals for multiple symbols
curl -X POST http://localhost:5001/api/signals/generate \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "GOOGL", "MSFT"], "days_back": 3}'

# Execute trade
curl -X POST http://localhost:5001/api/trade/execute \
  -H "Content-Type: application/json" \
  -d '{"signal": {"symbol": "AAPL", "signal": "BUY", "confidence": 0.85}}'
```

## 🎯 Advanced Features

### ML-Powered Analysis
- **Pattern Recognition**: Learns from historical trading patterns
- **Sentiment Analysis**: Combines VADER and TextBlob for accuracy
- **Feature Engineering**: Advanced features like news velocity, publisher diversity
- **Model Training**: Weekly model updates for improved predictions

### Risk Management
- **Position Sizing**: Kelly Criterion-based position sizing
- **Daily Loss Limits**: Automatic stop-loss at portfolio level
- **Diversification**: Maximum open positions limit
- **Real-time Monitoring**: Continuous risk assessment

### Multi-Source News
- **Yahoo Finance**: Primary news source
- **Finnhub**: Secondary source for better coverage
- **Automatic Deduplication**: No duplicate articles
- **Fallback Mechanism**: Continues if one source fails

## 📱 Frontend Dashboard

Access the trading dashboard at `http://localhost:5173` (or your Vite dev server port).

### Features:
- **Real-time Charts**: Signal distribution, performance metrics
- **Live Updates**: Auto-refresh every 30 seconds
- **Manual Analysis**: Analyze specific symbols on-demand
- **Trade Execution**: Execute signals directly from dashboard
- **Risk Monitoring**: Live risk metrics and alerts

## 🔧 N8N Workflow Setup

### 1. Access N8N UI
- Open `http://localhost:5678`
- Create new workflows or import from templates

### 2. Basic Workflow Structure
```
Schedule Trigger → HTTP Request → Function → HTTP Request → Telegram
     ↓              (API Call)     (Process)   (Execute)     (Alert)
   Every 15min     /api/signals   Data Proc   /api/trade   Message
```

### 3. Key N8N Nodes
- **Schedule Trigger**: For automated execution
- **HTTP Request**: Call your API endpoints
- **Function**: Process data and apply logic
- **Telegram**: Send notifications
- **Email**: Send alerts (alternative to Telegram)

## 📞 Telegram Integration

### Setup Bot
1. Message `@BotFather` on Telegram
2. Create new bot: `/newbot`
3. Get bot token from BotFather
4. Start chat with your bot
5. Get chat ID using: `https://api.telegram.org/bot<TOKEN>/getUpdates`

### Configuration
Add to `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 🚨 Alert Types

- **Trade Alerts**: New trade executions
- **Risk Alerts**: Loss limits, position limits
- **System Alerts**: Connection issues, errors
- **Market Updates**: Sentiment changes, recommendations

## 📈 Performance Monitoring

### Key Metrics
- **Signal Accuracy**: Win rate of generated signals
- **Response Time**: News analysis speed
- **API Uptime**: System availability
- **Risk Compliance**: Adherence to risk limits

### Logs
- **Application Logs**: `trading_bot.log`
- **N8N Logs**: Check N8N UI or logs directory
- **API Logs**: Flask server console output

## 🔒 Security Considerations

- **API Keys**: Store securely in environment variables
- **Rate Limiting**: Implement on API endpoints
- **Input Validation**: Validate all API inputs
- **Error Handling**: Comprehensive error handling
- **Backup**: Regular data backups

## 🚀 Production Deployment

### Docker Setup
```dockerfile
# Dockerfile for N8N API
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "n8n_api.py"]
```

### Environment Variables
- Use production-grade secret management
- Separate dev/staging/prod environments
- Enable HTTPS in production

## 🆘 Troubleshooting

### Common Issues

**N8N can't connect to API:**
- Check if Flask server is running on port 5001
- Verify CORS settings in Flask app
- Check firewall settings

**News analysis fails:**
- Verify API keys in `.env`
- Check internet connection
- Review API rate limits

**MT5 connection issues:**
- Verify MT5 credentials
- Ensure MT5 terminal is running
- Check server settings

**Telegram alerts not working:**
- Verify bot token and chat ID
- Check bot permissions
- Test bot manually first

## 📚 Additional Resources

- [N8N Documentation](https://docs.n8n.io/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)
- [Finnhub API](https://finnhub.io/docs/api)
- [MT5 Python Documentation](https://www.mql5.com/en/docs/integration/python_metatrader5)

## 🎯 Next Steps

1. **Test Individual Components**: Start with news analysis, then add trading
2. **Implement Risk Management**: Set appropriate limits for your strategy
3. **Monitor Performance**: Track accuracy and adjust parameters
4. **Add More Features**: Custom indicators, additional news sources
5. **Scale Up**: Add more symbols, optimize performance

---

**Happy Trading! 🚀📈**

For support or questions, check the logs and API responses first. Most issues can be resolved by verifying configuration and connectivity.
