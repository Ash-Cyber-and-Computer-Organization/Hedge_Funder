// MongoDB script to create collections for hedge_funder database
const database = 'hedge_funder';

// The current database to use.
use(database);

// Create collections for the hedge fund system
db.createCollection('trade_signals');
db.createCollection('portfolio');
db.createCollection('transactions');

// Create indexes for better performance
db.trade_signals.createIndex({ "ticker": 1, "timestamp": -1 });
db.portfolio.createIndex({ "ticker": 1, "timestamp": -1 });
db.transactions.createIndex({ "ticker": 1, "timestamp": -1 });

print("Collections created successfully");
// Note: Ensure that MongoDB server is running and you have the necessary permissions to create databases and collections.