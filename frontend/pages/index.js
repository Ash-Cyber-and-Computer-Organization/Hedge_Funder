// frontend/pages/index.js
import { useEffect, useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

export default function Dashboard() {
  const [data, setData] = useState({ balance: 0, equity: 0, recentTrades: [] });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('http://your-backend-api/balance');
        setData(res.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold text-gold">Trading Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="p-4 bg-bamboo-green rounded-lg shadow-lg">
            <h2 className="text-xl text-gold">Balance</h2>
            <p className="text-2xl">${data.balance.toFixed(2)}</p>
          </div>
          <div className="p-4 bg-bamboo-green rounded-lg shadow-lg">
            <h2 className="text-xl text-gold">Equity</h2>
            <p className="text-2xl">${data.equity.toFixed(2)}</p>
          </div>
          <div className="p-4 bg-bamboo-green rounded-lg shadow-lg">
            <h2 className="text-xl text-gold">Profit/Loss</h2>
            <p className="text-2xl">${(data.equity - data.balance).toFixed(2)}</p>
          </div>
        </div>
        <div className="mt-8">
          <h2 className="text-2xl text-gold">Recent Trades</h2>
          <table className="w-full mt-4 border-collapse">
            <thead>
              <tr className="bg-bamboo-green">
                <th className="p-2">Symbol</th>
                <th className="p-2">Action</th>
                <th className="p-2">Price</th>
              </tr>
            </thead>
            <tbody>
              {data.recentTrades.map((trade, index) => (
                <tr key={index} className="border-b border-gray-700">
                  <td className="p-2">{trade.symbol}</td>
                  <td className="p-2">{trade.action}</td>
                  <td className="p-2">{trade.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <Link href="/trades">
            <a className="mt-4 inline-block bg-gold text-gray-900 px-4 py-2 rounded">View All Trades</a>
          </Link>
        </div>
      </div>
    </div>
  );
}