#!/usr/bin/env python3
"""
Telegram Signal Trader
Processes trading signals received via Telegram and executes trades
"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import MetaTrader5 as mt5

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramSignalTrader:
    """Processes trading signals and executes trades via MT5"""

    def __init__(self):
        self.mt5_login = int(os.getenv('MT5_LOGIN', 0))
        self.mt5_password = os.getenv('MT5_PASSWORD')
        self.mt5_server = os.getenv('MT5_SERVER')
        self.connected = False

        # Connect to MT5
        self.connect_mt5()

    def connect_mt5(self):
        """Connect to MetaTrader 5 terminal"""
        if not mt5.initialize():
            logger.error("MT5 initialization failed")
            return False

        if self.mt5_login and self.mt5_password and self.mt5_server:
            authorized = mt5.login(self.mt5_login, self.mt5_password, self.mt5_server)
            if authorized:
                logger.info("MT5 connection successful")
                self.connected = True
                return True
            else:
                logger.error("MT5 login failed")
                return False
        else:
            logger.warning("MT5 credentials not configured")
            return False

    def disconnect_mt5(self):
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("MT5 disconnected")

    def parse_signal(self, signal_text):
        """Parse trading signal from text format"""
        try:
            # Expected format: "BUY AAPL SL=150.00 TP=160.00"
            parts = signal_text.upper().split()

            if len(parts) < 2:
                return None

            action = parts[0]  # BUY or SELL
            symbol = parts[1]   # AAPL

            # Default values
            sl = None
            tp = None
            volume = 0.01  # Default volume

            # Parse optional parameters
            for part in parts[2:]:
                if part.startswith('SL='):
                    sl = float(part.split('=')[1])
                elif part.startswith('TP='):
                    tp = float(part.split('=')[1])
                elif part.startswith('VOL='):
                    volume = float(part.split('=')[1])

            return {
                'action': action,
                'symbol': symbol,
                'sl': sl,
                'tp': tp,
                'volume': volume
            }

        except Exception as e:
            logger.error(f"Error parsing signal: {e}")
            return None

    def execute_trade(self, signal_data):
        """Execute trade based on signal data"""
        if not self.connected:
            logger.error("MT5 not connected")
            return False

        try:
            symbol = signal_data['symbol']
            action = signal_data['action']
            volume = signal_data.get('volume', 0.01)
            sl = signal_data.get('sl')
            tp = signal_data.get('tp')

            # Get symbol info
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"Symbol {symbol} not found")
                return False

            # Check if symbol is visible
            if not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    logger.error(f"Failed to select symbol {symbol}")
                    return False

            # Prepare order request
            order_type = mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL

            price = mt5.symbol_info_tick(symbol).ask if action == 'BUY' else mt5.symbol_info_tick(symbol).bid

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 10,
                "magic": 234000,
                "comment": f"Telegram Signal {datetime.now().strftime('%H:%M:%S')}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # Send order
            result = mt5.order_send(request)

            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"Trade executed successfully: {action} {symbol} at {price}")
                return True
            else:
                logger.error(f"Trade execution failed: {result.retcode}")
                return False

        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return False

    def process_signal(self, signal_text):
        """Process a trading signal from text"""
        logger.info(f"Processing signal: {signal_text}")

        # Parse signal
        signal_data = self.parse_signal(signal_text)

        if not signal_data:
            logger.error("Failed to parse signal")
            return False

        # Execute trade
        success = self.execute_trade(signal_data)

        return success

    def get_account_info(self):
        """Get account information"""
        if not self.connected:
            return None

        account_info = mt5.account_info()
        if account_info:
            return {
                'balance': account_info.balance,
                'equity': account_info.equity,
                'margin': account_info.margin,
                'margin_free': account_info.margin_free,
                'profit': account_info.profit
            }
        return None

    def get_positions(self):
        """Get current positions"""
        if not self.connected:
            return []

        positions = mt5.positions_get()
        if positions:
            return [{
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == mt5.POSITION_TYPE_BUY else 'SELL',
                'volume': pos.volume,
                'price_open': pos.price_open,
                'price_current': pos.price_current,
                'profit': pos.profit,
                'sl': pos.sl,
                'tp': pos.tp
            } for pos in positions]

        return []

# Global trader instance
signal_trader = TelegramSignalTrader()

def process_signal(signal_text):
    """Convenience function to process trading signals"""
    return signal_trader.process_signal(signal_text)

def test_connection():
    """Test MT5 connection"""
    return signal_trader.connected

if __name__ == '__main__':
    # Test connection
    if test_connection():
        print("✅ MT5 connection successful")

        # Get account info
        account = signal_trader.get_account_info()
        if account:
            print(f"Account Balance: ${account['balance']:.2f}")
            print(f"Account Equity: ${account['equity']:.2f}")

        # Get positions
        positions = signal_trader.get_positions()
        print(f"Open Positions: {len(positions)}")

    else:
        print("❌ MT5 connection failed")

    # Cleanup
    signal_trader.disconnect_mt5()
