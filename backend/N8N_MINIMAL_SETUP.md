# 🚀 Minimal N8N Integration Setup

## Overview

This is a clean, minimal implementation of n8n integration for automated trading with the following flow:

```
Frontend → Backend Webhook → N8N Workflow → Finnhub API → Signal Generation → Trade Execution → Telegram Alerts
```

## Files Created

- `n8n_minimal_api.py` - Minimal Flask API with core endpoints
- `n8n_minimal_workflow.json` - Basic n8n workflow template
- `telegram_bot.py` - Telegram notification system
- `telegram_signal_trader.py` - MT5 trading execution
- `test_finnhub_integration.py` - Finnhub API client and testing

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in backend directory:

```env
# Finnhub API
FINNHUB_API_KEY=your_finnhub_api_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# MT5 Trading
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server

# API Port
N8N_API_PORT=5001
```

### 3. Start the API Server

```bash
python n8n_minimal_api.py
```

The API will be available at `http://localhost:5001`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/webhook/news` | Receive news requests from frontend |
| POST | `/api/finnhub/news` | Fetch news from Finnhub |
| POST | `/api/signals/generate` | Generate trading signals |
| POST | `/api/trade/execute` | Execute trades |
| GET | `/api/monitoring/status` | System status |
| POST | `/api/alerts/send` | Send Telegram alerts |

## N8N Workflow Setup

### 1. Import Workflow

1. Start n8n: `n8n start`
2. Open `http://localhost:5678`
3. Create new workflow
4. Import `n8n_minimal_workflow.json`

### 2. Workflow Flow

```
Webhook → Finnhub News → Generate Signals → Check Confidence → Execute Trade → Send Alert
```

### 3. Test Workflow

Send a test request to the webhook:

```bash
curl -X POST http://localhost:5001/api/webhook/news \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'
```

## Testing

### Test Finnhub Integration

```bash
python test_finnhub_integration.py
```

### Test Telegram Bot

```bash
python telegram_bot.py
```

### Test MT5 Connection

```bash
python telegram_signal_trader.py
```

## Architecture

### Components

- **Frontend**: Sends news requests to backend webhook
- **Backend API**: Receives requests, processes data, executes trades
- **N8N Workflow**: Orchestrates the flow between services
- **Finnhub API**: Provides news and market data
- **MT5**: Executes trades
- **Telegram**: Sends notifications

### Data Flow

1. Frontend sends news request to `/api/webhook/news`
2. N8N workflow triggers and calls `/api/finnhub/news`
3. Backend fetches news from Finnhub and analyzes sentiment
4. N8N calls `/api/signals/generate` to create trading signals
5. If confidence > 60%, N8N calls `/api/trade/execute`
6. Backend executes trade via MT5 and sends Telegram alert

## Configuration

### Environment Variables

- `FINNHUB_API_KEY`: Your Finnhub API key
- `TELEGRAM_BOT_TOKEN`: Telegram bot token
- `TELEGRAM_CHAT_ID`: Telegram chat ID for notifications
- `MT5_LOGIN`: MT5 account login
- `MT5_PASSWORD`: MT5 account password
- `MT5_SERVER`: MT5 server address
- `N8N_API_PORT`: Port for the API server (default: 5001)

## Troubleshooting

### Common Issues

**API not responding:**
- Check if Flask server is running on port 5001
- Verify environment variables are set correctly

**Finnhub API errors:**
- Check your API key is valid
- Verify internet connection

**MT5 connection issues:**
- Ensure MT5 terminal is running
- Check login credentials

**Telegram not working:**
- Verify bot token and chat ID
- Test bot manually first

### Logs

Check the console output of the Flask server for detailed error messages and API call logs.

## Next Steps

1. **Test the workflow**: Send test requests and verify each step
2. **Customize signals**: Modify confidence thresholds and signal logic
3. **Add risk management**: Implement position sizing and stop-loss
4. **Expand symbols**: Add more symbols to monitor
5. **Add scheduling**: Set up automated execution intervals

## Support

For issues or questions:
1. Check the logs for error messages
2. Test individual components separately
3. Verify all environment variables are set
4. Ensure all services are running and accessible

---

**Happy Trading! 🚀📈**
