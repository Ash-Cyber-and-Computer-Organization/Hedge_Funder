// frontend/pages/trades.js
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function Trades() {
  const [trades, setTrades] = useState([]);
  const [chartData, setChartData] = useState({ labels: [], datasets: [] });

  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const res = await axios.get('http://your-backend-api/trades');
        setTrades(res.data);
        // Simulate Forex chart data for a selected pair (e.g., EURUSD)
        const chartRes = await axios.get('http://your-backend-api/chart/EURUSD');
        setChartData({
          labels: chartRes.data.labels, // Timestamps
          datasets: [
            {
              label: 'EURUSD Price',
              data: chartRes.data.prices,
              borderColor: '#D4A017',
              backgroundColor: 'rgba(212, 160, 23, 0.2)',
              fill: true,
            },
          ],
        });
      } catch (error) {
        console.error('Error fetching trades:', error);
      }
    };
    fetchTrades();
    const interval = setInterval(fetchTrades, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold text-gold">Ongoing Trades</h1>
        <div className="mt-6">
          <h2 className="text-2xl text-gold">Live Forex Chart (EURUSD)</h2>
          <div className="bg-bamboo-green p-4 rounded-lg">
            <Line data={chartData} options={{ responsive: true }} />
          </div>
        </div>
        <div className="mt-8">
          <h2 className="text-2xl text-gold">Active Trades</h2>
          <table className="w-full mt-4 border-collapse">
            <thead>
              <tr className="bg-bamboo-green">
                <th className="p-2">Symbol</th>
                <th className="p-2">Action</th>
                <th className="p-2">Price</th>
                <th className="p-2">Stop Loss</th>
                <th className="p-2">Take Profit</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade, index) => (
                <tr key={index} className="border-b border-gray-700">
                  <td className="p-2">{trade.symbol}</td>
                  <td className="p-2">{trade.action}</td>
                  <td className="p-2">{trade.price}</td>
                  <td className="p-2">{trade.sl}</td>
                  <td className="p-2">{trade.tp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}