import MetaTrader5 as mt5
import os
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# MetaTrader 5 Connection Settings (from .env file)
login = int(os.getenv("MT5_LOGIN", "5033134663"))  # Replace with your MT5 login
password = os.getenv("MT5_PASSWORD", "Ap*i6aAs")  # Replace with your MT5 password
server = os.getenv("MT5_SERVER", "MetaQuotes-Demo")  # Replace with your MT5 server

FIXED_LOT_SIZE = float(os.getenv("FIXED_LOT_SIZE", "0.2"))  # set lot size (e.g 0.2)
MAX_DAILY_TRADES = int(os.getenv("MAX_DAILY_TRADES", "10"))  # Set Maximum Trades

trade_count = 0  # Counter for daily trades

def process_signal(signal):
    """Process incoming trading signals."""
    global trade_count

    logger.info(f"Received signal: {signal}")

    if trade_count >= MAX_DAILY_TRADES:
        logger.warning(f"Daily trade limit reached. Current count: {trade_count}/{MAX_DAILY_TRADES}")
        return

    try:
        parts = signal.split()
        if len(parts) < 4:
            logger.error(f"Invalid signal format. Expected at least 4 parts, got {len(parts)}")
            return

        action = parts[0].upper()
        symbol = parts[1]
        sl = float(parts[2].split('=')[1])
        tp = float(parts[3].split('=')[1])

        logger.info(f"Parsed Signal: Action={action}, Symbol={symbol}, SL={sl}, TP={tp}")

        if action not in ["BUY", "SELL"]:
            logger.error(f"Invalid action '{action}'. Must be 'BUY' or 'SELL'")
            return

        success = place_trade(action, symbol, sl, tp)
        if success:
            trade_count += 1
            logger.info(f"Trade processed successfully. Daily count: {trade_count}/{MAX_DAILY_TRADES}")
        else:
            logger.error("Trade placement failed")

    except ValueError as e:
        logger.error(f"Error parsing signal values: {e}")
    except Exception as e:
        logger.error(f"Error processing signal: {e}")

def place_trade(action, symbol, sl, tp):
    """Place a trade in MetaTrader 5."""
    logger.info(f"Placing trade: Action={action}, Symbol={symbol}, SL={sl}, TP={tp}")

    try:
        # Initialize MT5 connection
        if not mt5.initialize(login=login, password=password, server=server):
            error_code, description = mt5.last_error()
            logger.error(f"Failed to initialize MT5: {error_code}, {description}")
            return False

        logger.info("MT5 connection established successfully")

        # Check symbol availability
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            logger.error(f"Symbol {symbol} not found in MT5")
            mt5.shutdown()
            return False

        logger.info(f"Symbol {symbol} found. Visible: {symbol_info.visible}")

        # Make symbol visible if needed
        if not symbol_info.visible:
            logger.info(f"Making symbol {symbol} visible")
            if not mt5.symbol_select(symbol, True):
                logger.error(f"Failed to select symbol {symbol}")
                mt5.shutdown()
                return False

        # Get current price
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            logger.error(f"Failed to get tick data for {symbol}")
            mt5.shutdown()
            return False

        # Define order type and price
        order_type = 0 if action.upper() == "BUY" else 1  # 0 for BUY, 1 for SELL
        price = tick.ask if order_type == 0 else tick.bid

        logger.info(f"Order details: Type={order_type}, Price={price}, Lot Size={FIXED_LOT_SIZE}")

        # Prepare trade request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": FIXED_LOT_SIZE,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 10,
            "magic": 234000,
            "comment": "Telegram Signal Trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        logger.info(f"Sending trade request: {request}")

        # Send order
        result = mt5.order_send(request)

        if result is None:
            error_code, description = mt5.last_error()
            logger.error(f"Order send failed: {error_code}, {description}")
            mt5.shutdown()
            return False

        logger.info(f"Order result: retcode={result.retcode}, deal={result.deal}, order={result.order}")

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Order failed: retcode={result.retcode}, message={result.comment}")
            mt5.shutdown()
            return False
        else:
            logger.info(f"Trade placed successfully: Deal ID={result.deal}, Order ID={result.order}")
            mt5.shutdown()
            return True

    except Exception as e:
        logger.error(f"Error in place_trade: {e}")
        try:
            mt5.shutdown()
        except:
            pass
        return False

def test_connection():
    """Test MT5 connection and basic functionality."""
    logger.info("Testing MT5 connection...")

    try:
        if not mt5.initialize(login=login, password=password, server=server):
            error_code, description = mt5.last_error()
            logger.error(f"MT5 connection test failed: {error_code}, {description}")
            return False

        logger.info("MT5 connection test successful")

        # Test account info
        account_info = mt5.account_info()
        if account_info:
            logger.info(f"Account: {account_info.login}, Balance: {account_info.balance}")
        else:
            logger.warning("Could not retrieve account info")

        mt5.shutdown()
        return True

    except Exception as e:
        logger.error(f"Connection test error: {e}")
        return False

def interactive_test():
    """Interactive testing mode for debugging."""
    logger.info("Starting interactive test mode")
    logger.info("Type trading signals in format: BUY EURUSD SL=1.0500 TP=1.0700")
    logger.info("Type 'test' to test connection, 'quit' to exit")

    while True:
        try:
            signal = input("\nEnter signal: ").strip()
            if signal.lower() == 'quit':
                break
            elif signal.lower() == 'test':
                test_connection()
            elif signal:
                process_signal(signal)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            break
        except Exception as e:
            logger.error(f"Interactive test error: {e}")

if __name__ == "__main__":
    logger.info("=== Telegram Signal Trader Algorithm ===")
    logger.info(f"Configuration: Login={login}, Server={server}, Lot Size={FIXED_LOT_SIZE}, Max Trades={MAX_DAILY_TRADES}")

    # Test connection on startup
    if test_connection():
        logger.info("MT5 connection verified. Algorithm ready.")
    else:
        logger.error("MT5 connection failed. Check your credentials and MT5 installation.")

    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test()
    else:
        logger.info("Running in module mode. Import and use process_signal() function.")
        logger.info("Example: process_signal('BUY EURUSD SL=1.0500 TP=1.0700')")
