import os
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DataStorage:
    def __init__(self):
        """Initialize MongoDB connection and collections"""
        try:
            # MongoDB connection string from environment
            mongo_url = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017/')
            db_name = os.environ.get('MONGODB_DATABASE', 'hedge_funder')

            self.client = MongoClient(mongo_url)
            self.db = self.client[db_name]

            # Test connection
            self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB successfully")

            # Collections
            self.market_data = self.db.market_data
            self.intraday_data = self.db.intraday_data
            self.real_time_prices = self.db.real_time_prices

            # Create indexes for better performance
            self._create_indexes()

        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise

    def _create_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            # Market data indexes
            self.market_data.create_index([('ticker', 1), ('date', -1)])
            self.market_data.create_index([('timestamp', -1)])

            # Intraday data indexes
            self.intraday_data.create_index([('ticker', 1), ('date', -1)])
            self.intraday_data.create_index([('timestamp', -1)])

            # Real-time prices indexes
            self.real_time_prices.create_index([('ticker', 1), ('timestamp', -1)])

            logger.info("✅ Database indexes created successfully")

        except Exception as e:
            logger.error(f"❌ Error creating indexes: {e}")

    def store_market_data(self, ticker, data, source_api):
        """Store historical market data with metadata"""
        try:
            documents = []
            for date, row in data.iterrows():
                doc = {
                    'ticker': ticker,
                    'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                    'open': float(row.get('Open', 0)),
                    'high': float(row.get('High', 0)),
                    'low': float(row.get('Low', 0)),
                    'close': float(row.get('Close', 0)),
                    'volume': float(row.get('Volume', 0)),
                    'source_api': source_api,
                    'timestamp': datetime.utcnow(),
                    'data_type': 'historical'
                }
                documents.append(doc)

            if documents:
                result = self.market_data.insert_many(documents)
                logger.info(f"✅ Stored {len(documents)} market data records for {ticker}")
                return len(result.inserted_ids)

        except Exception as e:
            logger.error(f"❌ Error storing market data for {ticker}: {e}")
            return 0

    def store_intraday_data(self, ticker, data, source_api):
        """Store intraday data with metadata"""
        try:
            documents = []
            for date, row in data.iterrows():
                doc = {
                    'ticker': ticker,
                    'date': date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(date, 'strftime') else str(date),
                    'open': float(row.get('Open', 0)),
                    'high': float(row.get('High', 0)),
                    'low': float(row.get('Low', 0)),
                    'close': float(row.get('Close', 0)),
                    'volume': float(row.get('Volume', 0)),
                    'source_api': source_api,
                    'timestamp': datetime.utcnow(),
                    'data_type': 'intraday'
                }
                documents.append(doc)

            if documents:
                result = self.intraday_data.insert_many(documents)
                logger.info(f"✅ Stored {len(documents)} intraday data records for {ticker}")
                return len(result.inserted_ids)

        except Exception as e:
            logger.error(f"❌ Error storing intraday data for {ticker}: {e}")
            return 0

    def store_real_time_prices(self, ticker, price_data, source_api):
        """Store real-time price data"""
        try:
            doc = {
                'ticker': ticker,
                'current_price': float(price_data.get('current_price', 0)),
                'previous_close': float(price_data.get('previous_close', 0)),
                'change': float(price_data.get('change', 0)),
                'change_percent': float(price_data.get('change_percent', 0)),
                'volume': float(price_data.get('volume', 0)),
                'source_api': source_api,
                'timestamp': datetime.utcnow(),
                'data_type': 'real_time'
            }

            result = self.real_time_prices.insert_one(doc)
            logger.info(f"✅ Stored real-time price data for {ticker}")
            return result.inserted_id

        except Exception as e:
            logger.error(f"❌ Error storing real-time price for {ticker}: {e}")
            return None

    def get_cached_market_data(self, ticker, days_back=30):
        """Retrieve cached market data for a ticker"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_back)
            cursor = self.market_data.find({
                'ticker': ticker,
                'timestamp': {'$gte': cutoff_date}
            }).sort('date', -1)

            data = list(cursor)
            if data:
                logger.info(f"✅ Retrieved {len(data)} cached market data records for {ticker}")
                return data
            else:
                logger.info(f"ℹ️ No cached market data found for {ticker}")
                return []

        except Exception as e:
            logger.error(f"❌ Error retrieving cached market data for {ticker}: {e}")
            return []

    def get_cached_intraday_data(self, ticker, hours_back=24):
        """Retrieve cached intraday data for a ticker"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
            cursor = self.intraday_data.find({
                'ticker': ticker,
                'timestamp': {'$gte': cutoff_time}
            }).sort('date', -1)

            data = list(cursor)
            if data:
                logger.info(f"✅ Retrieved {len(data)} cached intraday data records for {ticker}")
                return data
            else:
                logger.info(f"ℹ️ No cached intraday data found for {ticker}")
                return []

        except Exception as e:
            logger.error(f"❌ Error retrieving cached intraday data for {ticker}: {e}")
            return []

    def get_cached_real_time_prices(self, ticker, minutes_back=60):
        """Retrieve cached real-time prices for a ticker"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=minutes_back)
            cursor = self.real_time_prices.find({
                'ticker': ticker,
                'timestamp': {'$gte': cutoff_time}
            }).sort('timestamp', -1)

            data = list(cursor)
            if data:
                logger.info(f"✅ Retrieved {len(data)} cached real-time price records for {ticker}")
                return data
            else:
                logger.info(f"ℹ️ No cached real-time prices found for {ticker}")
                return []

        except Exception as e:
            logger.error(f"❌ Error retrieving cached real-time prices for {ticker}: {e}")
            return []

    def cleanup_old_data(self, days_to_keep=90):
        """Clean up old data to prevent database bloat"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)

            # Clean up market data
            market_result = self.market_data.delete_many({
                'timestamp': {'$lt': cutoff_date}
            })

            # Clean up intraday data
            intraday_result = self.intraday_data.delete_many({
                'timestamp': {'$lt': cutoff_date}
            })

            # Clean up real-time prices (keep less historical data)
            realtime_cutoff = datetime.utcnow() - timedelta(days=7)
            realtime_result = self.real_time_prices.delete_many({
                'timestamp': {'$lt': realtime_cutoff}
            })

            logger.info(f"✅ Cleaned up old data: Market({market_result.deleted_count}), "
                       f"Intraday({intraday_result.deleted_count}), "
                       f"Real-time({realtime_result.deleted_count})")

        except Exception as e:
            logger.error(f"❌ Error cleaning up old data: {e}")

    def get_database_stats(self):
        """Get database statistics"""
        try:
            stats = {
                'market_data_count': self.market_data.count_documents({}),
                'intraday_data_count': self.intraday_data.count_documents({}),
                'real_time_prices_count': self.real_time_prices.count_documents({}),
                'total_records': (self.market_data.count_documents({}) +
                                self.intraday_data.count_documents({}) +
                                self.real_time_prices.count_documents({}))
            }
            logger.info(f"📊 Database stats: {stats}")
            return stats

        except Exception as e:
            logger.error(f"❌ Error getting database stats: {e}")
            return {}

# Global instance
data_storage = None

def get_data_storage():
    """Get or create data storage instance"""
    global data_storage
    if data_storage is None:
        data_storage = DataStorage()
    return data_storage

def init_data_storage():
    """Initialize data storage - call this at application startup"""
    try:
        storage = get_data_storage()
        storage.cleanup_old_data()  # Clean up old data on startup
        logger.info("✅ Data storage initialized successfully")
        return storage
    except Exception as e:
        logger.error(f"❌ Failed to initialize data storage: {e}")
        return None
