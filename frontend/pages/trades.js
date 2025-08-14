import React from "react";
import ModernLayout from "../components/ModernLayout";

export default function Trades() {
  return (
    <ModernLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-white">Trading Dashboard</h1>

        <div className="bg-dark-800/50 backdrop-blur-sm rounded-xl p-6 border border-dark-700">
          <h3 className="text-lg font-semibold text-white">Balance</h3>
          <p className="text-2xl font-bold text-primary-400">$0.00</p>
        </div>

        <div className="bg-dark-800/50 backdrop-blur-sm rounded-xl p-6 border border-dark-700">
          <h3 className="text-lg font-semibold text-white">Equity</h3>
          <p className="text-2xl font-bold text-primary-400">$0.00</p>
        </div>

        <div className="bg-dark-800/50 backdrop-blur-sm rounded-xl p-6 border border-dark-700">
          <h3 className="text-lg font-semibold text-white">Profit/Loss</h3>
          <p className="text-2xl font-bold text-primary-400">$0.00</p>
        </div>

        <div className="bg-dark-800/50 backdrop-blur-sm rounded-xl p-6 border border-dark-700">
          <h3 className="text-lg font-semibold text-white">Recent Trades</h3>
          <table className="min-w-full">
            <thead>
              <tr className="bg-dark-700 text-white">
                <th className="px-4 py-2">Symbol</th>
                <th className="px-4 py-2">Action</th>
                <th className="px-4 py-2">Price</th>
              </tr>
            </thead>
            <tbody>
              {/* Recent trades rows go here */}
            </tbody>
          </table>
          <Link href="/trades" className="text-primary-400 hover:underline">View All Trades</Link>
        </div>
      </div>
    </ModernLayout>
  );
}
