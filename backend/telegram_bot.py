#!/usr/bin/env python3
"""
Telegram Bot for Trading Alerts and Signals
Provides Telegram integration for sending alerts and receiving commands
"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Telegram Bot for trading alerts and signals"""

    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram credentials not found in environment variables")

    def send_message(self, message, parse_mode='Markdown'):
        """Send a message to the configured chat"""
        if not self.bot_token or not self.chat_id:
            logger.error("Telegram credentials not configured")
            return False

        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True
            }

            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()

            logger.info(f"Telegram message sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def send_alert(self, alert_type, message):
        """Send formatted alert message"""
        emoji_map = {
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'SUCCESS': '✅',
            'CRITICAL': '🚨'
        }

        emoji = emoji_map.get(alert_type.upper(), '📢')
        formatted_message = f"{emoji} **{alert_type.upper()} ALERT**\n\n{message}"

        return self.send_message(formatted_message)

    def send_signal_alert(self, symbol, signal, confidence, reason=""):
        """Send trading signal alert"""
        confidence_pct = f"{confidence * 100:.1f}%"

        message = f"🚀 **TRADING SIGNAL**\n\n"
        message += f"📊 **Symbol**: {symbol}\n"
        message += f"🎯 **Signal**: {signal}\n"
        message += f"💯 **Confidence**: {confidence_pct}\n"

        if reason:
            message += f"📝 **Reason**: {reason}\n"

        message += f"⏰ **Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        return self.send_message(message)

    def send_performance_update(self, pnl, total_signals, success_rate):
        """Send performance update"""
        pnl_emoji = "📈" if pnl >= 0 else "📉"
        pnl_formatted = f"{pnl_emoji} **P&L**: ${pnl:.2f}"

        message = f"📊 **PERFORMANCE UPDATE**\n\n"
        message += f"{pnl_formatted}\n"
        message += f"🎯 **Total Signals**: {total_signals}\n"
        message += f"💯 **Success Rate**: {success_rate:.1%}\n"
        message += f"⏰ **Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        return self.send_message(message)

# Global bot instance
telegram_bot = TelegramBot()

def send_telegram_alert(message, alert_type='INFO'):
    """Convenience function to send alerts"""
    return telegram_bot.send_alert(alert_type, message)

def send_signal_notification(symbol, signal, confidence, reason=""):
    """Convenience function to send signal notifications"""
    return telegram_bot.send_signal_alert(symbol, signal, confidence, reason)

if __name__ == '__main__':
    # Test the bot
    test_message = "🧪 **Test Message**\n\nThis is a test message from the Telegram bot."
    success = telegram_bot.send_message(test_message)

    if success:
        print("✅ Telegram bot test successful")
    else:
        print("❌ Telegram bot test failed - check credentials")
