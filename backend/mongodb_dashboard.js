// MongoDB Playground Dashboard for Hedge Funder
// This script creates a dashboard view by querying collections and aggregating data
// Run this in MongoDB Atlas Playground or Compass to visualize your hedge fund data
// References the Flask dashboard structure: latest signals, portfolio summary, recent transactions, database stats

const database = 'hedge_funder';

// Switch to the database
use(database);

// 1. DASHBOARD OVERVIEW - Database Stats
print("📊 DASHBOARD OVERVIEW - Database Statistics");
const stats = {
  market_data_count: db.market_data.countDocuments({}),
  intraday_data_count: db.intraday_data.countDocuments({}),
  real_time_prices_count: db.real_time_prices.countDocuments({}),
  trade_signals_count: db.trade_signals.countDocuments({}),
  portfolio_count: db.portfolio.countDocuments({}),
  transactions_count: db.transactions.countDocuments({}),
  total_records: db.market_data.countDocuments({}) + db.intraday_data.countDocuments({}) + db.real_time_prices.countDocuments({}) + db.trade_signals.countDocuments({}) + db.portfolio.countDocuments({}) + db.transactions.countDocuments({})
};
printjson(stats);

// 2. LATEST TRADE SIGNALS (Top 10 recent signals, like dashboard's latest_signals)
print("\n🚦 LATEST TRADE SIGNALS (Top 10)");
const latestSignals = db.trade_signals.find({}).sort({ timestamp: -1 }).limit(10).toArray();
printjson(latestSignals);

// 3. PORTFOLIO SUMMARY (Current positions and total value)
print("\n💼 PORTFOLIO SUMMARY");
const portfolio = db.portfolio.find({ user_id: "default" }).toArray();
let totalPortfolioValue = 0;
portfolio.forEach(pos => {
  totalPortfolioValue += pos.current_value || 0;
});
print("Total Portfolio Value: $" + totalPortfolioValue.toFixed(2));
printjson(portfolio);

// 4. RECENT TRANSACTIONS (Top 10 recent, like dashboard's recent_transactions)
print("\n💳 RECENT TRANSACTIONS (Top 10)");
const recentTransactions = db.transactions.find({ user_id: "default" }).sort({ timestamp: -1 }).limit(10).toArray();
printjson(recentTransactions);

// 5. REAL-TIME PRICES SUMMARY (Latest prices for monitored tickers)
print("\n📈 REAL-TIME PRICES SUMMARY (Latest for AAPL, GOOGL, MSFT, TSLA)");
const tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA'];
tickers.forEach(ticker => {
  const latestPrice = db.real_time_prices.find({ ticker: ticker }).sort({ timestamp: -1 }).limit(1).toArray();
  if (latestPrice.length > 0) {
    print(`${ticker}: $${latestPrice[0].current_price} (Change: ${latestPrice[0].change_percent.toFixed(2)}%)`);
    printjson(latestPrice[0]);
  } else {
    print(`${ticker}: No recent data`);
  }
});

// 6. AGGREGATED INSIGHTS - Buy/Sell Signal Counts (Last 24 hours)
print("\n📋 AGGREGATED INSIGHTS - Signal Counts (Last 24 hours)");
const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
const signalCounts = db.trade_signals.aggregate([
  { $match: { timestamp: { $gte: oneDayAgo } } },
  { $group: { _id: "$action", count: { $sum: 1 } } }
]).toArray();
printjson(signalCounts);

// 7. PORTFOLIO PERFORMANCE (Simple P&L calculation if avg_price and current_value available)
print("\n📊 PORTFOLIO PERFORMANCE");
let totalPnL = 0;
portfolio.forEach(pos => {
  if (pos.avg_price && pos.current_value) {
    const quantity = pos.quantity || 1;
    const pnl = (pos.current_value - (pos.avg_price * quantity));
    totalPnL += pnl;
    print(`${pos.ticker}: P&L $${pnl.toFixed(2)}`);
  }
});
print(`Total Portfolio P&L: $${totalPnL.toFixed(2)}`);

// 8. VISUALIZATION READY DATA - Export to JSON for frontend import
print("\n💾 EXPORT ALL DASHBOARD DATA AS JSON (Copy this for your Flask dashboard)");
const fullDashboardData = {
  stats: stats,
  latest_signals: latestSignals,
  portfolio: portfolio,
  total_portfolio_value: totalPortfolioValue,
  recent_transactions: recentTransactions,
  real_time_prices: {},
  signal_counts: signalCounts,
  total_pnl: totalPnL
};
tickers.forEach(ticker => {
  const latest = db.real_time_prices.find({ ticker: ticker }).sort({ timestamp: -1 }).limit(1).toArray();
  if (latest.length > 0) {
    fullDashboardData.real_time_prices[ticker] = latest[0];
  }
});
printjson(fullDashboardData);

print("\n🎉 Dashboard script complete! Run this in MongoDB Playground to view your hedge fund data.");
