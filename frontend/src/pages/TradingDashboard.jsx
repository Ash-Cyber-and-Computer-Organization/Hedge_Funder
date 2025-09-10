import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, BarChart, Bar, ResponsiveContainer
} from 'recharts';

const TradingDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedTimeframe, setSelectedTimeframe] = useState('1D');

  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  useEffect(() => {
    fetchDashboardData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5001/api/monitoring/dashboard');
      setDashboardData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const analyzeSymbol = async (symbol) => {
    try {
      const response = await axios.post('http://localhost:5001/api/finnhub/news', {
        symbol: symbol,
        days_back: 3
      });

      const sentiment = response.data.sentiment_analysis;
      let sentimentText = 'N/A';

      if (sentiment && typeof sentiment === 'object') {
        if (sentiment.overall_sentiment) {
          sentimentText = `${sentiment.overall_sentiment} (${sentiment.confidence_score?.toFixed(2) || 'N/A'})`;
        } else if (sentiment.sentiment) {
          sentimentText = sentiment.sentiment;
        }
      } else if (typeof sentiment === 'string') {
        sentimentText = sentiment;
      }

      alert(`Analysis complete for ${symbol}. Found ${response.data.total_articles || 0} articles. Sentiment: ${sentimentText}`);
      fetchDashboardData(); // Refresh data
    } catch (err) {
      alert('Analysis failed: ' + err.message);
    }
  };

  const executeTrade = async (signal) => {
    try {
      const response = await axios.post('http://localhost:5001/api/trade/execute', {
        signal: signal
      });
      alert(`Trade executed: ${response.data.action} ${response.data.symbol}`);
      fetchDashboardData(); // Refresh data
    } catch (err) {
      alert('Trade execution failed: ' + err.message);
    }
  };

  const executeN8NWorkflow = async () => {
    try {
      // Trigger the N8N cloud webhook for trading signals
      const webhookUrl = 'https://ash1industries.app.n8n.cloud/webhook/trading-signals';
      const response = await axios.post(webhookUrl, {
        symbols: ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA'],
        days_back: 3
      });
      alert('N8N workflow executed successfully.');
      fetchDashboardData(); // Refresh data after workflow execution
    } catch (err) {
      alert('Failed to execute N8N workflow: ' + err.message);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-xl">Loading Trading Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️ {error}</div>
          <button
            onClick={fetchDashboardData}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const { system_status, performance, recent_signals, risk_metrics } = dashboardData || {};

  // Prepare chart data
  const signalDistribution = recent_signals?.reduce((acc, signal) => {
    acc[signal.signal] = (acc[signal.signal] || 0) + 1;
    return acc;
  }, {});

  const signalChartData = Object.entries(signalDistribution || {}).map(([signal, count]) => ({
    signal,
    count
  }));

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">🚀 Advanced Trading Dashboard</h1>
          <p className="text-gray-400">Real-time N8N-powered trading with AI analysis</p>
          <div className="mt-4 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 xl:grid-cols-10 gap-2">
            {/* Major Tech Stocks */}
            <button
              onClick={() => analyzeSymbol('AAPL')}
              className="bg-blue-600 hover:bg-blue-700 px-2 py-2 rounded-lg text-xs"
            >
              📱 AAPL
            </button>
            <button
              onClick={() => analyzeSymbol('GOOGL')}
              className="bg-green-600 hover:bg-green-700 px-2 py-2 rounded-lg text-xs"
            >
              🔍 GOOGL
            </button>
            <button
              onClick={() => analyzeSymbol('MSFT')}
              className="bg-purple-600 hover:bg-purple-700 px-2 py-2 rounded-lg text-xs"
            >
              💻 MSFT
            </button>
            <button
              onClick={() => analyzeSymbol('TSLA')}
              className="bg-red-600 hover:bg-red-700 px-2 py-2 rounded-lg text-xs"
            >
              🚗 TSLA
            </button>
            <button
              onClick={() => analyzeSymbol('NVDA')}
              className="bg-green-500 hover:bg-green-600 px-2 py-2 rounded-lg text-xs"
            >
              🎮 NVDA
            </button>
            <button
              onClick={() => analyzeSymbol('AMZN')}
              className="bg-orange-600 hover:bg-orange-700 px-2 py-2 rounded-lg text-xs"
            >
              📦 AMZN
            </button>
            <button
              onClick={() => analyzeSymbol('META')}
              className="bg-blue-500 hover:bg-blue-600 px-2 py-2 rounded-lg text-xs"
            >
              👥 META
            </button>
            <button
              onClick={() => analyzeSymbol('NFLX')}
              className="bg-red-500 hover:bg-red-600 px-2 py-2 rounded-lg text-xs"
            >
              🎬 NFLX
            </button>

            {/* Semiconductor & Hardware */}
            <button
              onClick={() => analyzeSymbol('AMD')}
              className="bg-red-600 hover:bg-red-700 px-2 py-2 rounded-lg text-xs"
            >
              🔧 AMD
            </button>
            <button
              onClick={() => analyzeSymbol('INTC')}
              className="bg-blue-700 hover:bg-blue-800 px-2 py-2 rounded-lg text-xs"
            >
              💾 INTC
            </button>
            <button
              onClick={() => analyzeSymbol('QCOM')}
              className="bg-indigo-600 hover:bg-indigo-700 px-2 py-2 rounded-lg text-xs"
            >
              📡 QCOM
            </button>
            <button
              onClick={() => analyzeSymbol('CRM')}
              className="bg-teal-600 hover:bg-teal-700 px-2 py-2 rounded-lg text-xs"
            >
              ☁️ CRM
            </button>

            {/* Entertainment & Media */}
            <button
              onClick={() => analyzeSymbol('DIS')}
              className="bg-blue-600 hover:bg-blue-700 px-2 py-2 rounded-lg text-xs"
            >
              🎢 DIS
            </button>
            <button
              onClick={() => analyzeSymbol('SPOT')}
              className="bg-green-700 hover:bg-green-800 px-2 py-2 rounded-lg text-xs"
            >
              🎵 SPOT
            </button>

            {/* Financial Services */}
            <button
              onClick={() => analyzeSymbol('JPM')}
              className="bg-slate-600 hover:bg-slate-700 px-2 py-2 rounded-lg text-xs"
            >
              🏦 JPM
            </button>
            <button
              onClick={() => analyzeSymbol('V')}
              className="bg-cyan-600 hover:bg-cyan-700 px-2 py-2 rounded-lg text-xs"
            >
              💳 V
            </button>
            <button
              onClick={() => analyzeSymbol('COIN')}
              className="bg-yellow-600 hover:bg-yellow-700 px-2 py-2 rounded-lg text-xs"
            >
              ₿ COIN
            </button>

            {/* Major Cryptocurrencies */}
            <button
              onClick={() => analyzeSymbol('BTC-USD')}
              className="bg-yellow-500 hover:bg-yellow-600 px-2 py-2 rounded-lg text-xs"
            >
              ₿ BTC
            </button>
            <button
              onClick={() => analyzeSymbol('ETH-USD')}
              className="bg-gray-600 hover:bg-gray-700 px-2 py-2 rounded-lg text-xs"
            >
              Ξ ETH
            </button>
            <button
              onClick={() => analyzeSymbol('ADA-USD')}
              className="bg-blue-400 hover:bg-blue-500 px-2 py-2 rounded-lg text-xs"
            >
              ₳ ADA
            </button>
            <button
              onClick={() => analyzeSymbol('BNB-USD')}
              className="bg-yellow-600 hover:bg-yellow-700 px-2 py-2 rounded-lg text-xs"
            >
              🟡 BNB
            </button>
            <button
              onClick={() => analyzeSymbol('SOL-USD')}
              className="bg-purple-500 hover:bg-purple-600 px-2 py-2 rounded-lg text-xs"
            >
              ◎ SOL
            </button>
            <button
              onClick={() => analyzeSymbol('MATIC-USD')}
              className="bg-purple-600 hover:bg-purple-700 px-2 py-2 rounded-lg text-xs"
            >
              🟣 MATIC
            </button>
            <button
              onClick={() => analyzeSymbol('AVAX-USD')}
              className="bg-red-400 hover:bg-red-500 px-2 py-2 rounded-lg text-xs"
            >
              🏔️ AVAX
            </button>
            <button
              onClick={() => analyzeSymbol('DOT-USD')}
              className="bg-pink-600 hover:bg-pink-700 px-2 py-2 rounded-lg text-xs"
            >
              🔗 DOT
            </button>
            <button
              onClick={() => analyzeSymbol('LINK-USD')}
              className="bg-blue-600 hover:bg-blue-700 px-2 py-2 rounded-lg text-xs"
            >
              🔗 LINK
            </button>
            <button
              onClick={() => analyzeSymbol('UNI-USD')}
              className="bg-pink-500 hover:bg-pink-600 px-2 py-2 rounded-lg text-xs"
            >
              🦄 UNI
            </button>

            {/* ETFs and Indices */}
            <button
              onClick={() => analyzeSymbol('SPY')}
              className="bg-green-700 hover:bg-green-800 px-2 py-2 rounded-lg text-xs"
            >
              📈 SPY
            </button>
            <button
              onClick={() => analyzeSymbol('QQQ')}
              className="bg-indigo-600 hover:bg-indigo-700 px-2 py-2 rounded-lg text-xs"
            >
              💎 QQQ
            </button>
            <button
              onClick={() => analyzeSymbol('IWM')}
              className="bg-orange-600 hover:bg-orange-700 px-2 py-2 rounded-lg text-xs"
            >
              🏢 IWM
            </button>
            <button
              onClick={() => analyzeSymbol('VTI')}
              className="bg-emerald-600 hover:bg-emerald-700 px-2 py-2 rounded-lg text-xs"
            >
              🌍 VTI
            </button>

            {/* Commodities */}
            <button
              onClick={() => analyzeSymbol('GLD')}
              className="bg-yellow-600 hover:bg-yellow-700 px-2 py-2 rounded-lg text-xs"
            >
              🏆 GLD
            </button>
            <button
              onClick={() => analyzeSymbol('SLV')}
              className="bg-gray-500 hover:bg-gray-600 px-2 py-2 rounded-lg text-xs"
            >
              🥈 SLV
            </button>
            <button
              onClick={() => analyzeSymbol('USO')}
              className="bg-black hover:bg-gray-800 px-2 py-2 rounded-lg text-xs"
            >
              🛢️ USO
            </button>

            {/* International Markets */}
            <button
              onClick={() => analyzeSymbol('EWJ')}
              className="bg-red-600 hover:bg-red-700 px-2 py-2 rounded-lg text-xs"
            >
              🇯🇵 EWJ
            </button>
            <button
              onClick={() => analyzeSymbol('EWG')}
              className="bg-yellow-600 hover:bg-yellow-700 px-2 py-2 rounded-lg text-xs"
            >
              🇩🇪 EWG
            </button>
            <button
              onClick={() => analyzeSymbol('EFA')}
              className="bg-blue-600 hover:bg-blue-700 px-2 py-2 rounded-lg text-xs"
            >
              🌍 EFA
            </button>

            {/* Bonds and Fixed Income */}
            <button
              onClick={() => analyzeSymbol('BND')}
              className="bg-green-600 hover:bg-green-700 px-2 py-2 rounded-lg text-xs"
            >
              📊 BND
            </button>
            <button
              onClick={() => analyzeSymbol('TLT')}
              className="bg-blue-700 hover:bg-blue-800 px-2 py-2 rounded-lg text-xs"
            >
              🏛️ TLT
            </button>
            <button
              onClick={() => analyzeSymbol('LQD')}
              className="bg-indigo-600 hover:bg-indigo-700 px-2 py-2 rounded-lg text-xs"
            >
              💼 LQD
            </button>

            {/* Real Estate */}
            <button
              onClick={() => analyzeSymbol('VNQ')}
              className="bg-orange-600 hover:bg-orange-700 px-2 py-2 rounded-lg text-xs"
            >
              🏠 VNQ
            </button>
            <button
              onClick={() => analyzeSymbol('IYR')}
              className="bg-red-600 hover:bg-red-700 px-2 py-2 rounded-lg text-xs"
            >
              🏢 IYR
            </button>
          </div>
        </div>

        {/* System Status */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-4">🔗 System Status</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>MT5 Connection:</span>
                <span className={system_status?.mt5_connection ? 'text-green-500' : 'text-red-500'}>
                  {system_status?.mt5_connection ? '✅ Connected' : '❌ Disconnected'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>News Sources:</span>
                <span className="text-blue-400">{system_status?.news_sources?.length || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Active Workflows:</span>
                <span className="text-green-400">{system_status?.active_workflows?.length || 0}</span>
              </div>
              <div className="text-sm text-gray-400 mt-2">
                Last Update: {new Date(system_status?.last_update).toLocaleString()}
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-4">📊 Performance</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Total Signals:</span>
                <span className="text-blue-400">{performance?.total_signals || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Success Rate:</span>
                <span className="text-green-400">{((performance?.success_rate || 0) * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span>Daily P&L:</span>
                <span className={performance?.daily_pnl >= 0 ? 'text-green-500' : 'text-red-500'}>
                  ${performance?.daily_pnl?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Open Positions:</span>
                <span className="text-yellow-400">{performance?.open_positions || 0}</span>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-4">⚡ Risk Management</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Max Daily Loss:</span>
                <span className="text-red-400">${risk_metrics?.max_daily_loss || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Max Position Size:</span>
                <span className="text-yellow-400">{((risk_metrics?.max_position_size || 0) * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span>Current Positions:</span>
                <span className="text-blue-400">{risk_metrics?.current_positions || 0}</span>
              </div>
              <div className="text-sm text-gray-400 mt-2">
                Risk Level: Low
              </div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Signal Distribution */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-4">📈 Signal Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={signalChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ signal, count }) => `${signal}: ${count}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {signalChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Recent Signals */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-4">📋 Recent Signals</h3>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {recent_signals?.slice(0, 10).map((signal, index) => (
                <div key={index} className="flex justify-between items-center p-3 bg-gray-700 rounded">
                  <div>
                    <span className="font-semibold">{signal.symbol}</span>
                    <span className={`ml-2 px-2 py-1 rounded text-sm ${
                      signal.signal === 'BUY' ? 'bg-green-600' :
                      signal.signal === 'SELL' ? 'bg-red-600' : 'bg-yellow-600'
                    }`}>
                      {signal.signal}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-400">
                      {(signal.confidence * 100).toFixed(1)}% confidence
                    </div>
                    <button
                      onClick={() => executeTrade(signal)}
                      className="mt-1 bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-sm"
                    >
                      Execute
                    </button>
                  </div>
                </div>
              )) || <p className="text-gray-400">No recent signals</p>}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">⚡ Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => analyzeSymbol(prompt('Enter symbol:'))}
              className="bg-blue-600 hover:bg-blue-700 p-4 rounded-lg text-center"
            >
              <div className="text-2xl mb-2">🔍</div>
              <div>Custom Analysis</div>
            </button>
            <button
              onClick={fetchDashboardData}
              className="bg-green-600 hover:bg-green-700 p-4 rounded-lg text-center"
            >
              <div className="text-2xl mb-2">🔄</div>
              <div>Refresh Data</div>
            </button>
            <button
              onClick={() => window.open('https://ash1industries.app.n8n.cloud', '_blank')}
              className="bg-purple-600 hover:bg-purple-700 p-4 rounded-lg text-center"
              title="Open the N8N Cloud dashboard in a new tab"
            >
              <div className="text-2xl mb-2">🤖</div>
              <div>Open N8N Cloud</div>
            </button>
            <button
              onClick={executeN8NWorkflow}
              className="bg-indigo-600 hover:bg-indigo-700 p-4 rounded-lg text-center"
              title="Trigger the N8N trading signals workflow"
            >
              <div className="text-2xl mb-2">⚡</div>
              <div>Execute Workflow</div>
            </button>
            <a
              href="https://ash1industries.app.n8n.cloud"
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 block text-blue-400 underline"
            >
              View N8N Workflow Dashboard
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradingDashboard;
