# News-Based Trading System

This document describes the new news-based trading system that integrates Yahoo Finance news analysis with your existing MetaTrader 5 trading setup.

## Overview

The news-based trading system consists of three main components:

1. **NewsAnalyzer** (`news_analyzer.py`) - Fetches and analyzes financial news
2. **NewsTradingIntegration** (`news_trading_integration.py`) - Combines news analysis with trading execution
3. **Configuration** (`.env`) - Environment variables for customization

## Features

- **Multi-source News Fetching**: Gets news from Yahoo Finance (primary) and Finnhub (optional)
- **Sentiment Analysis**: Analyzes news sentiment using keyword-based scoring
- **Signal Generation**: Generates BUY/SELL/HOLD signals based on news sentiment
- **MT5 Integration**: Seamlessly integrates with your existing MetaTrader 5 setup
- **Configurable Parameters**: Customizable thresholds, symbols, and intervals
- **Continuous Monitoring**: Automated news monitoring and trading execution

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Test Setup**:
   ```bash
   python news_trading_integration.py --test
   ```

## Configuration

### Required Settings

```env
# MetaTrader 5 (copy from your existing setup)
MT5_LOGIN=your_login
MT5_PASSWORD=your_password
MT5_SERVER=your_server
FIXED_LOT_SIZE=0.2
MAX_DAILY_TRADES=10

# News Analysis
SENTIMENT_THRESHOLD=0.1          # Minimum sentiment score for signal (0.1 = 10%)
NEWS_LOOKBACK_DAYS=7            # Days of news to analyze
MIN_NEWS_ARTICLES=3             # Minimum articles needed for reliable signal
MONITOR_SYMBOLS=AAPL,GOOGL,MSFT # Symbols to monitor
ANALYSIS_INTERVAL_MINUTES=60    # Analysis frequency
AUTO_TRADE=false                # Enable automatic trading
```

### Optional Settings

```env
# Additional news source (requires API key from finnhub.io)
FINNHUB_API_KEY=your_api_key

# N8N Integration (for workflow automation)
N8N_CLOUD_URL=https://your-n8n-instance.com
N8N_WEBHOOK_PATH=/webhook/trading-signal
N8N_API_KEY=your_n8n_api_key
```

## Usage

### Test the System

```bash
# Test MT5 connection and news analysis
python news_trading_integration.py --test
```

### Manual Analysis

```python
from news_analyzer import NewsAnalyzer

analyzer = NewsAnalyzer()
result = analyzer.analyze_symbol('AAPL', days_back=3)

if result and result['signal']:
    print(f"Signal: {result['signal']['signal']}")
    print(f"Confidence: {result['signal']['confidence']:.3f}")
```

### Start Continuous Monitoring

```bash
# Start automated news monitoring and trading
python news_trading_integration.py --monitor
```

### Generate Signals for Specific Symbols

```python
from news_trading_integration import NewsTradingIntegration

integration = NewsTradingIntegration()
signals = integration.generate_news_signals(['AAPL', 'GOOGL', 'MSFT'])

for signal in signals:
    print(f"{signal['symbol']}: {signal['signal']} ({signal['confidence']:.3f})")
```

## How It Works

### News Fetching
1. Fetches recent news articles from Yahoo Finance
2. Optionally supplements with Finnhub news
3. Filters articles by publication date
4. Removes duplicate articles

### Sentiment Analysis
1. Analyzes article titles and summaries
2. Uses keyword-based sentiment scoring
3. Counts positive vs negative keywords
4. Calculates overall sentiment score

### Signal Generation
1. Requires minimum number of articles for reliability
2. Compares sentiment score against threshold
3. Generates BUY/SELL/HOLD signals
4. Includes confidence score and reasoning

### Trading Integration
1. Formats signals for existing MT5 system
2. Executes trades automatically (if enabled)
3. Logs all activities
4. Respects daily trade limits

## Signal Format

Generated signals follow your existing format:
```
BUY AAPL SL=0.00 TP=0.00
SELL GOOGL SL=0.00 TP=0.00
```

Note: SL/TP values are set to 0.00 for news-based signals. You may want to implement dynamic stop-loss/take-profit logic.

## Customization

### Adding New Symbols

Update the `MONITOR_SYMBOLS` in your `.env` file:
```env
MONITOR_SYMBOLS=AAPL,GOOGL,MSFT,TSLA,AMZN,NVDA
```

### Adjusting Sentiment Threshold

Lower values = more signals, higher values = fewer but more confident signals:
```env
SENTIMENT_THRESHOLD=0.2  # More conservative
SENTIMENT_THRESHOLD=0.05 # More aggressive
```

### Changing Analysis Frequency

```env
ANALYSIS_INTERVAL_MINUTES=30  # More frequent analysis
ANALYSIS_INTERVAL_MINUTES=120 # Less frequent analysis
```

## Safety Features

- **Minimum Article Threshold**: Requires multiple articles for reliable signals
- **Daily Trade Limits**: Respects your existing `MAX_DAILY_TRADES` setting
- **Connection Testing**: Verifies MT5 connection before trading
- **Error Handling**: Comprehensive logging and error recovery
- **Manual Override**: Can disable auto-trading for testing

## Monitoring and Logging

All activities are logged to:
- Console output
- `trading_bot.log` file
- Individual analysis results

Monitor the logs to:
- Track signal generation
- Review trade execution
- Debug connection issues
- Analyze system performance

## Troubleshooting

### No News Found
- Check symbol format (use uppercase: AAPL, not aapl)
- Verify internet connection
- Try different symbols
- Check Yahoo Finance API availability

### MT5 Connection Issues
- Verify login credentials in `.env`
- Check MT5 server settings
- Ensure MT5 is running
- Test connection with: `python telegram_signal_trader.py`

### Low Signal Confidence
- Reduce `SENTIMENT_THRESHOLD`
- Increase `NEWS_LOOKBACK_DAYS`
- Check `MIN_NEWS_ARTICLES` setting
- Monitor news volume for symbols

### Performance Issues
- Increase `ANALYSIS_INTERVAL_MINUTES`
- Reduce number of monitored symbols
- Check system resources
- Monitor API rate limits

## Integration with N8N

For advanced workflow automation, the system can integrate with N8N:

1. Set up N8N cloud instance
2. Configure webhook endpoints
3. Enable N8N settings in `.env`
4. Create workflows for:
   - Signal processing
   - Risk management
   - Alert notifications
   - Performance tracking

See `N8N_CLOUD_SETUP_GUIDE.md` for detailed setup instructions.

## Next Steps

1. **Test with Paper Trading**: Enable demo mode in MT5
2. **Backtest Signals**: Analyze historical performance
3. **Refine Parameters**: Adjust thresholds based on results
4. **Add Risk Management**: Implement position sizing
5. **Expand News Sources**: Add more financial news APIs
6. **Machine Learning**: Enhance sentiment analysis with ML models

## Support

For issues or questions:
1. Check the logs in `trading_bot.log`
2. Run diagnostic tests: `python news_trading_integration.py --test`
3. Verify configuration in `.env`
4. Ensure all dependencies are installed

The system is designed to be modular and extensible. Each component can be enhanced or replaced independently.
