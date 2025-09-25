# Quick Steps to Create Hedge Funder Dashboard in MongoDB Charts

## 1. Create Dashboard
- Go to MongoDB Atlas → Charts → "Create New Dashboard"
- Name: "Hedge Funder Trading Dashboard"
- Select your cluster and `hedge_funder` database

## 2. Database Overview Chart
- Add Chart → Column Chart
- Data Source: `market_data` collection
- Pipeline:
```javascript
[{$group: {_id: null, count: {$sum: 1}}}]
```
- X: "_id" → Y: "count"
- Title: "Total Market Data Records"

## 3. Trade Signals Distribution
- Add Chart → Pie Chart
- Data Source: `trade_signals` collection
- Pipeline:
```javascript
[{$group: {_id: "$action", count: {$sum: 1}}}]
```
- Label: "_id" → Value: "count"
- Title: "Buy/Sell/Hold Signals"

## 4. Recent Transactions Table
- Add Chart → Table Chart
- Data Source: `transactions` collection
- Pipeline:
```javascript
[{$sort: {timestamp: -1}}, {$limit: 10}]
```
- Columns: ticker, action, quantity, price, total_value, timestamp
- Title: "Latest Transactions"

## 5. Portfolio Performance
- Add Chart → Line Chart
- Data Source: `portfolio` collection
- Pipeline:
```javascript
[{$sort: {timestamp: 1}}, {$group: {_id: {$dateToString: {format: "%Y-%m-%d", date: "$timestamp"}}, value: {$sum: "$current_value"}}}]
```
- X: "_id" → Y: "value"
- Title: "Portfolio Value Trend"

## 6. Real-Time Prices
- Add Chart → Bar Chart
- Data Source: `real_time_prices` collection
- Pipeline:
```javascript
[{$sort: {timestamp: -1}}, {$group: {_id: "$ticker", price: {$first: "$current_price"}, change: {$first: "$change_percent"}}}]
```
- X: "_id" → Y: "change"
- Title: "Price Change %"

## 7. Add Filters
- Add Filter: Date Range on "timestamp"
- Add Filter: Select on "ticker"

## 8. Publish
- Click "Publish" to share dashboard
