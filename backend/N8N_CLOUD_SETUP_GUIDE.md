# N8N Cloud Integration Setup Guide

This guide will help you link your local Hedge Funder backend with your N8N cloud instance at `https://ash1industries.app.n8n.cloud`.

## Prerequisites

1. **N8N Cloud Account**: You have access to `https://ash1industries.app.n8n.cloud`
2. **Ngrok Account**: Sign up at [ngrok.com](https://ngrok.com) for secure tunneling
3. **Python Environment**: Your backend is running on port 5001

## Step 1: Install Ngrok

```bash
# Install ngrok globally
npm install -g ngrok

# Or download from ngrok website
# https://ngrok.com/download
```

## Step 2: Authenticate Ngrok

```bash
# Authenticate with your ngrok account
ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN
```

## Step 3: Start Your Local Backend

```bash
cd backend
python n8n_api.py
```

Verify it's running:
```bash
curl http://localhost:5001/api/health
```

## Step 4: Expose Local Backend with Ngrok

```bash
# Start ngrok tunnel to port 5001
ngrok http 5001
```

You'll see output like:
```
ngrok by @inconshreveable

Session Status                online
Account                       your-account (Plan: Free)
Version                       3.1.0
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://abc123.ngrok.io -> http://localhost:5001
Forwarding                    https://abc123.ngrok.io -> http://localhost:5001

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy your ngrok URL** (e.g., `https://abc123.ngrok.io`)

## Step 5: Update Configuration

Update your `backend/.env` file with the ngrok URL:

```env
NGROK_URL=https://abc123.ngrok.io
```

Update `backend/n8n_workflow_config.json` to replace `your-ngrok-url.ngrok.io` with your actual ngrok URL.

## Step 6: Create N8N Cloud Workflows

### Workflow 1: News Analysis & Signal Generation

1. **Go to N8N Cloud**: https://ash1industries.app.n8n.cloud
2. **Create New Workflow**
3. **Add Webhook Trigger**:
   - HTTP Method: POST
   - Path: `/trading-signals`
   - Authentication: None (for now)

4. **Add Schedule Trigger**:
   - Rule: Every 15 minutes
   - Timezone: Your timezone

5. **Add HTTP Request Node**:
   - Method: POST
   - URL: `https://abc123.ngrok.io/api/signals/generate`
   - Body:
     ```json
     {
       "symbols": ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"],
       "days_back": 3
     }
     ```
   - Headers:
     ```json
     {
       "Content-Type": "application/json"
     }
     ```

6. **Add Function Node** (Process Signals):
   ```javascript
   const signals = $node["HTTP Request"].json.signals;

   // Filter high-confidence signals
   let validSignals = signals.filter(signal => signal.confidence > 0.6 && signal.risk_validated);

   let message = '🚀 **Trading Signals Generated**\n\n';

   if (validSignals.length > 0) {
     validSignals.forEach(signal => {
       message += `📊 **${signal.symbol}**: ${signal.signal}\n`;
       message += `🎯 Confidence: ${(signal.confidence * 100).toFixed(1)}%\n`;
       message += `📝 Reason: ${signal.reason}\n\n`;
     });
   } else {
     message += '⚠️ No high-confidence signals found\n';
   }

   return [{ json: { message, signals: validSignals } }];
   ```

7. **Add Telegram Node** (if configured):
   - Resource: Message
   - Chat ID: Your chat ID
   - Text: `{{$node["Function"].json.message}}`

8. **Save and Activate** the workflow

### Workflow 2: Risk Monitoring & Alerts

1. **Create New Workflow**
2. **Add Schedule Trigger**: Every 5 minutes
3. **Add HTTP Request Node**:
   - URL: `https://abc123.ngrok.io/api/monitoring/dashboard`
   - Method: GET

4. **Add Function Node** (Check Risk):
   ```javascript
   const data = $node["HTTP Request"].json;
   const riskMetrics = data.risk_metrics;
   const performance = data.performance;

   let alerts = [];

   // Check daily loss limit
   if (performance.daily_pnl < -riskMetrics.max_daily_loss * 0.8) {
     alerts.push({
       type: 'CRITICAL',
       message: `🚨 **CRITICAL: Daily Loss Alert**\nCurrent P&L: $${performance.daily_pnl}\nLimit: $${riskMetrics.max_daily_loss}`
     });
   }

   // Check position limits
   if (riskMetrics.current_positions >= riskMetrics.max_position_size * 10) {
     alerts.push({
       type: 'WARNING',
       message: `⚠️ **Position Limit Warning**\nCurrent Positions: ${riskMetrics.current_positions}\nMax Allowed: ${riskMetrics.max_position_size * 10}`
     });
   }

   return [{ json: { alerts, data } }];
   ```

5. **Add Telegram Node** for alerts
6. **Save and Activate**

### Workflow 3: Market Sentiment Analysis

1. **Create New Workflow**
2. **Add Schedule Trigger**: Every 2 hours
3. **Add HTTP Request Node**:
   - URL: `https://abc123.ngrok.io/api/news/analyze`
   - Method: POST
   - Body: `{"symbol": "^GSPC", "days_back": 1}`

4. **Add Function Node** (Format Sentiment):
   ```javascript
   const analysis = $node["HTTP Request"].json;

   if (!analysis || analysis.error) {
     return [{ json: { message: '❌ Market sentiment analysis failed', sentiment: 'UNKNOWN' } }];
   }

   const sentiment = analysis.sentiment_data.overall_score;
   const articleCount = analysis.sentiment_data.article_count;

   let sentimentEmoji = '😐';
   let sentimentText = 'NEUTRAL';

   if (sentiment > 0.2) {
     sentimentEmoji = '📈';
     sentimentText = 'BULLISH';
   } else if (sentiment < -0.2) {
     sentimentEmoji = '📉';
     sentimentText = 'BEARISH';
   }

   let message = `${sentimentEmoji} **Market Sentiment Update**\n\n`;
   message += `📊 **S&P 500 Sentiment**: ${sentimentText}\n`;
   message += `🎯 **Score**: ${(sentiment * 100).toFixed(1)}%\n`;
   message += `📰 **Articles Analyzed**: ${articleCount}\n`;
   message += `⏰ **Analysis Time**: ${new Date().toLocaleString()}`;

   return [{ json: { message, sentiment: sentimentText, score: sentiment } }];
   ```

5. **Add Telegram Node**
6. **Save and Activate**

## Step 7: Test the Integration

### Test Backend Endpoints

```bash
# Test health
curl https://abc123.ngrok.io/api/health

# Test signal generation
curl -X POST https://abc123.ngrok.io/api/signals/generate \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL"], "days_back": 3}'

# Test dashboard
curl https://abc123.ngrok.io/api/monitoring/dashboard
```

### Test N8N Workflows

1. **Manual Test**: Click "Execute Workflow" in N8N cloud
2. **Check Logs**: Monitor the execution logs in N8N
3. **Verify Telegram**: Check if you receive notifications

## Step 8: Configure Telegram Bot (Optional)

1. **Create Bot**: Message @BotFather on Telegram
2. **Get Token**: `/newbot` and follow instructions
3. **Get Chat ID**: Start a chat with your bot and visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. **Update .env**:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

## Troubleshooting

### Common Issues

1. **Ngrok Connection Issues**:
   ```bash
   # Restart ngrok
   ngrok http 5001

   # Check ngrok status
   curl http://localhost:4040/api/tunnels
   ```

2. **CORS Errors**: Ensure your backend has CORS enabled (it should be)

3. **Webhook Timeouts**: Increase timeout in N8N HTTP Request nodes to 30 seconds

4. **Rate Limiting**: N8N cloud has rate limits; space out your workflows

### Monitoring

- **Ngrok Dashboard**: http://localhost:4040 for tunnel monitoring
- **N8N Cloud Logs**: Check execution logs in your workflows
- **Backend Logs**: Monitor your Flask app logs

## Production Deployment

For production, consider:

1. **Vercel Deployment**: Deploy backend to Vercel for stable URLs
2. **Database**: Add persistent storage for signals and performance data
3. **Authentication**: Add API key authentication for N8N requests
4. **Monitoring**: Set up proper logging and alerting

## Next Steps

1. Test all workflows manually
2. Enable automatic scheduling
3. Monitor performance and adjust parameters
4. Add more sophisticated risk management
5. Implement trade execution automation

Your N8N cloud is now linked with your local backend! 🎉
