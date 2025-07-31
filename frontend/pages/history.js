// frontend/pages/history.js
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get('http://your-backend-api/history');
        setHistory(res.data);
      } catch (error) {
        console.error('Error fetching history:', error);
      }
    };
    fetchHistory();
  }, []);

  const downloadCSV = () => {
    const csv = ['Symbol,Action,Price,SL,TP,Timestamp']
      .concat(history.map((trade) => `${trade.symbol},${trade.action},${trade.price},${trade.sl},${trade.tp},${trade.timestamp}`))
      .join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'trade_history.csv';
    a.click();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold text-gold">Trade History</h1>
        <button onClick={downloadCSV} className="mt-4 bg-gold text-gray-900 px-4 py-2 rounded">
          Download CSV
        </button>
        <table className="w-full mt-4 border-collapse">
          <thead>
            <tr className="bg-bamboo-green">
              <th className="p-2">Symbol</th>
              <th className="p-2">Action</th>
              <th className="p-2">Price</th>
              <th className="p-2">SL</th>
              <th className="p-2">TP</th>
              <th className="p-2">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {history.map((trade, index) => (
              <tr key={index} className="border-b border-gray-700">
                <td className="p-2">{trade.symbol}</td>
                <td className="p-2">{trade.action}</td>
                <td className="p-2">{trade.price}</td>
                <td className="p-2">{trade.sl}</td>
                <td className="p-2">{trade.tp}</td>
                <td className="p-2">{trade.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}