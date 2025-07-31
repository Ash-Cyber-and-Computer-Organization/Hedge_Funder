// frontend/pages/balance.js
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Balance() {
  const [balance, setBalance] = useState({ balance: 0, equity: 0, margin: 0 });

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const res = await axios.get('http://your-backend-api/balance');
        setBalance(res.data);
      } catch (error) {
        console.error('Error fetching balance:', error);
      }
    };
    fetchBalance();
    const interval = setInterval(fetchBalance, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold text-gold">Account Balance</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="p-4 bg-bamboo-green rounded-lg shadow-lg">
            <h2 className="text-xl text-gold">Balance</h2>
            <p className="text-2xl">${balance.balance.toFixed(2)}</p>
          </div>
          <div className="p-4 bg-bamboo-green rounded-lg shadow-lg">
            <h2 className="text-xl text-gold">Equity</h2>
            <p className="text-2xl">${balance.equity.toFixed(2)}</p>
          </div>
          <div className="p-4 bg-bamboo-green rounded-lg shadow-lg">
            <h2 className="text-xl text-gold">Margin</h2>
            <p className="text-2xl">${balance.margin.toFixed(2)}</p>
          </div>
        </div>
      </div>
    </div>
  );
}