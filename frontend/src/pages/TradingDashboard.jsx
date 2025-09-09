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
