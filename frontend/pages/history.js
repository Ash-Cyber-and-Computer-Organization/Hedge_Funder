import React from 'react';

const History = () => {
  const mockHistory = [
    { id: 1, action: 'Deposit', amount: 2000, date: '2025-07-15' },
    { id: 2, action: 'Withdraw', amount: 1000, date: '2025-07-16' },
    { id: 3, action: 'Profit Share', amount: 500, date: '2025-07-17' },
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg p-4">
      <h2 className="text-lg font-semibold mb-2">Transaction History</h2>
      <ul className="space-y-2 max-h-64 overflow-y-auto">
        {mockHistory.map(item => (
          <li
            key={item.id}
            className="border rounded-md p-2 hover:bg-gray-50 flex justify-between items-center"
          >
            <div>
              <p className="font-medium">{item.action}</p>
              <p className="text-xs text-gray-500">{item.date}</p>
            </div>
            <span className="text-sm font-bold">₦{item.amount.toLocaleString()}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
