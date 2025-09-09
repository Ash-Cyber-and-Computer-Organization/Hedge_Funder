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
      const response = await axios.post('http://localhost:5001/api/news/analyze', {
        symbol: symbol,
        days_back: 3
      });
      alert(`Analysis complete for ${symbol}. Signal: ${response.data.final_signal?.signal || 'HOLD'}`);
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
          <div className="mt-4 flex gap-4">
            <button
              onClick={() => analyzeSymbol('AAPL')}
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
            >
              Analyze AAPL
            </button>
            <button
              onClick={() => analyzeSymbol('GOOGL')}
              className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
            >
              Analyze GOOGL
            </button>
            <button
              onClick={() => analyzeSymbol('MSFT')}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg"
            >
              Analyze MSFT
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
            >
              <div className="text-2xl mb-2">🤖</div>
              <div>Open N8N Cloud</div>
            </button>
            <button
              onClick={executeN8NWorkflow}
              className="bg-indigo-600 hover:bg-indigo-700 p-4 rounded-lg text-center"
            >
              <div className="text-2xl mb-2">⚡</div>
              <div>Execute Workflow</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradingDashboard;
