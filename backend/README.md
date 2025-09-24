# Hedge Funder Backend - MongoDB Integration

This backend provides a comprehensive market analysis system with MongoDB caching for improved performance and data persistence.

## Features

- **Real-time Stock Data**: Fetch live stock prices from multiple APIs (Finnhub, Alpha Vantage, Twelve Data)
- **Historical Data Caching**: Store and retrieve historical market data with MongoDB
- **Intraday Data Support**: Cache and retrieve intraday trading data
- **Technical Analysis**: Built-in indicators (SMA, EMA, RSI) for trading decisions
- **Rate Limiting**: Intelligent rate limiting to respect API constraints
- **Data Persistence**: All data stored in MongoDB for reliability and performance

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. MongoDB Setup

1. **Install MongoDB** (if not already installed):
   - Download from [MongoDB Community Server](https://www.mongodb.com/try/download/community)
   - Or use Docker: `docker run -d -p 27017:27017 --name mongodb mongo:latest`

2. **Start MongoDB**:
   - Windows: Run `mongod.exe` from your MongoDB installation directory
   - Linux/Mac: `sudo systemctl start mongod` or `brew services start mongodb-community`

3. **Verify Connection**:
   ```bash
   mongo --eval "db.runCommand('ismaster')"
   ```

### 3. Environment Configuration

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Update `.env` with your configuration**:
   ```env
   # MongoDB Configuration
   MONGODB_URL=mongodb://localhost:27017/
   MONGODB_DATABASE=hedge_funder

   # API Keys (get these from respective services)
   FINNHUB_API_KEY=your_finnhub_api_key_here
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
   TWELVE_DATA_API_KEY=your_twelve_data_api_key_here

   # Data Configuration
   DEFAULT_TICKERS=AAPL,GOOGL,MSFT,TSLA
   CACHE_DAYS=30
   CACHE_HOURS=24
   CACHE_MINUTES=60
   ```

### 4. Get API Keys

- **Finnhub**: Sign up at [finnhub.io](https://finnhub.io/) for real-time data
- **Alpha Vantage**: Get free API key at [alphavantage.co](https://www.alphavantage.co/support/#api-key)
- **Twelve Data**: Register at [twelvedata.com](https://twelvedata.com/) for intraday data

### 5. Run Tests

Test the MongoDB integration:
```bash
python test_mongodb_integration.py
```

## Usage

### Basic Market Analysis

```python
from Market Analysis Algorithm.market_analysis import run_market_analysis

# Run analysis for default tickers
result = run_market_analysis()
print(result)

# Run analysis for specific tickers
result = run_market_analysis(['AAPL', 'GOOGL'])
```

### Fetch Real-time Prices

```python
from Market Analysis Algorithm.market_analysis import get_real_time_prices

prices = get_real_time_prices(['AAPL', 'MSFT'])
print(prices)
```

### Fetch Historical Data

```python
from Market Analysis Algorithm.market_analysis import fetch_stock_data_batch

data = fetch_stock_data_batch(['AAPL'], start_date='2024-01-01', end_date='2024-12-31')
print(data)
```

### Fetch Intraday Data

```python
from Market Analysis Algorithm.market_analysis import intra_day_data

data = intra_day_data(['AAPL'], period='1d')
print(data)
```

## Data Storage

The system automatically caches data in MongoDB:

- **Market Data**: Historical daily data cached for 30 days
- **Intraday Data**: Intraday data cached for 24 hours
- **Real-time Prices**: Real-time prices cached for 60 minutes

### Manual Data Management

```python
from data_storage import get_data_storage

storage = get_data_storage()

# Get database statistics
stats = storage.get_database_stats()

# Clean up old data (older than 90 days)
storage.cleanup_old_data(days_to_keep=90)
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Sources   │───▶│ Market Analysis  │───▶│   MongoDB       │
│                 │    │ Algorithm        │    │   Storage       │
│ • Finnhub       │    │                  │    │                 │
│ • Alpha Vantage │    │ • Rate Limiting  │    │ • Market Data   │
│ • Twelve Data   │    │ • Data Caching   │    │ • Intraday Data │
│                 │    │ • Technical      │    │ • Real-time     │
│                 │    │   Analysis       │    │   Prices        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Performance Benefits

- **Reduced API Calls**: Cached data eliminates redundant API requests
- **Faster Response Times**: Local MongoDB queries are much faster than external API calls
- **Cost Savings**: Fewer API calls mean lower costs for paid services
- **Reliability**: Data persists even if external APIs are unavailable
- **Scalability**: MongoDB can handle large volumes of financial data efficiently

## Monitoring

The system provides comprehensive logging:

- Connection status and errors
- Data storage and retrieval operations
- API rate limiting and retry attempts
- Cache hit/miss ratios

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**:
   - Ensure MongoDB is running on the specified port
   - Check `MONGODB_URL` in `.env` file
   - Verify network connectivity

2. **API Rate Limits**:
   - The system includes built-in rate limiting
   - Check API key quotas and limits
   - Monitor logs for rate limit warnings

3. **Missing Data**:
   - Verify API keys are correctly configured
   - Check ticker symbols are valid
   - Review logs for specific error messages

### Debug Mode

Enable debug logging by modifying the logging configuration:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the logs for error messages
- Ensure all dependencies are installed correctly
- Verify API keys and MongoDB configuration
