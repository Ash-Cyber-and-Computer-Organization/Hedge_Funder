# Telegram Signal Trader Algorithm

This is a simplified trading algorithm that processes trading signals and executes trades on MetaTrader 5.

## Features

- Processes trading signals in the format: `ACTION SYMBOL SL=STOPLOSS TP=TAKEPROFIT`
- Executes trades on MetaTrader 5 platform
- Daily trade limit protection
- Comprehensive logging
- Environment-based configuration

## Signal Format

The algorithm expects signals in the following format:
```
BUY EURUSD SL=1.0500 TP=1.0700
SELL GBPUSD SL=1.2500 TP=1.2300
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy the environment template:
```bash
cp .env.example .env
```

3. Configure your MetaTrader 5 credentials in `.env`:
```env
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server
FIXED_LOT_SIZE=0.2
MAX_DAILY_TRADES=10
```

## Usage

### Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your MT5 credentials
```

3. **Test connection:**
```bash
python run_trader.py --test
```

4. **Run interactive mode:**
```bash
python run_trader.py --interactive
```

### Running Options

#### Using the Run Script (Recommended)

```bash
# Test MT5 connection
python run_trader.py --test

# Process a single signal
python run_trader.py --signal "BUY EURUSD SL=1.0500 TP=1.0700"

# Interactive testing mode
python run_trader.py --interactive

# Run demo signals (simulation)
python run_trader.py --demo
```

#### Direct Python Execution

```bash
# Basic module test
python telegram_signal_trader.py

# Interactive mode
python telegram_signal_trader.py --interactive
```

#### As a Python Module

```python
from telegram_signal_trader import process_signal, test_connection

# Test connection
if test_connection():
    print("MT5 connected successfully!")

# Process a trading signal
signal = "BUY EURUSD SL=1.0500 TP=1.0700"
process_signal(signal)
```

## Functions

### `process_signal(signal: str)`
Processes an incoming trading signal and executes the trade if valid.

**Parameters:**
- `signal` (str): Trading signal in the format "ACTION SYMBOL SL=STOPLOSS TP=TAKEPROFIT"

**Example:**
```python
process_signal("BUY EURUSD SL=1.0500 TP=1.0700")
```

### `place_trade(action: str, symbol: str, sl: float, tp: float)`
Places a trade on MetaTrader 5.

**Parameters:**
- `action` (str): "BUY" or "SELL"
- `symbol` (str): Trading symbol (e.g., "EURUSD")
- `sl` (float): Stop loss price
- `tp` (float): Take profit price

## Configuration

All configuration is done through environment variables:

- `MT5_LOGIN`: Your MetaTrader 5 login ID
- `MT5_PASSWORD`: Your MetaTrader 5 password
- `MT5_SERVER`: Your MetaTrader 5 server
- `FIXED_LOT_SIZE`: Lot size for each trade (default: 0.2)
- `MAX_DAILY_TRADES`: Maximum trades per day (default: 10)

## Error Handling

The algorithm includes comprehensive error handling for:
- Invalid signal formats
- MetaTrader 5 connection issues
- Symbol not found errors
- Daily trade limit exceeded
- Order execution failures

## Logging

All activities are logged to the console including:
- Received signals
- Parsed signal components
- Trade execution results
- Error messages

## Safety Features

- Daily trade limit to prevent overtrading
- Input validation for signal format
- MetaTrader 5 connection verification
- Symbol availability checking
- Comprehensive error handling

## Debugging and Troubleshooting

### Common Issues

1. **MT5 Connection Failed**
   - Ensure MetaTrader 5 is installed and running
   - Check your login credentials in `.env`
   - Verify your MT5 server is correct
   - Make sure your account has trading permissions

2. **Symbol Not Found**
   - Check if the symbol exists in your MT5 platform
   - Some symbols may need to be added manually in MT5
   - Verify the symbol name format (e.g., "EURUSD", not "EUR/USD")

3. **Order Failed**
   - Check your account balance
   - Verify stop loss and take profit levels are reasonable
   - Ensure the market is open for the symbol
   - Check if you have sufficient margin

### Debug Commands

```bash
# Test basic connection
python run_trader.py --test

# Run with detailed logging
python telegram_signal_trader.py  # Check trading_bot.log file

# Test with demo signals
python run_trader.py --demo

# Interactive debugging
python run_trader.py --interactive
```

### Log Files

- `trading_bot.log`: Contains detailed logs of all operations
- Console output: Real-time logging during execution

### Environment Variables Debug

If you're having issues with environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()
print("MT5_LOGIN:", os.getenv("MT5_LOGIN"))
print("MT5_SERVER:", os.getenv("MT5_SERVER"))
print("FIXED_LOT_SIZE:", os.getenv("FIXED_LOT_SIZE"))
```

## Dependencies

- MetaTrader5: For trading platform integration
- python-dotenv: For environment variable management
