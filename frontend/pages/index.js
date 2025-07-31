import React from "react";
import Footer from "../components/Footer";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#0A0F0D] text-white font-sans">
      <div className="bg-[#1A2E28] py-6 px-4 shadow-md">
        <h1 className="text-2xl font-bold text-green-400">Elite Trading</h1>
        <nav className="mt-2 space-x-4 text-sm text-gray-300">
          <a href="/" className="hover:text-green-500">Dashboard</a>
          <a href="/trades" className="hover:text-green-500">Trades</a>
          <a href="/history" className="hover:text-green-500">History</a>
          <a href="/balance" className="hover:text-green-500">Balance</a>
        </nav>
      </div>

      <main className="p-4 space-y-6">
        <section className="bg-[#132019] p-4 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold text-green-300">Balance</h2>
          <p className="text-lg mt-1">$0.00</p>
        </section>

        <section className="bg-[#132019] p-4 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold text-green-300">Equity</h2>
          <p className="text-lg mt-1">$0.00</p>
        </section>

        <section className="bg-[#132019] p-4 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold text-green-300">Profit/Loss</h2>
          <p className="text-lg mt-1">$0.00</p>
        </section>

        <section className="bg-[#132019] p-4 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold text-green-300 mb-3">Recent Trades</h2>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-400">
                <th>Symbol</th>
                <th>Action</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              <tr className="text-white">
                <td colSpan="3" className="py-2">No recent trades available.</td>
              </tr>
            </tbody>
          </table>
          <a href="/trades" className="text-sm text-green-400 hover:underline mt-2 block">View All Trades</a>
        </section>
      </main>

      <Footer />
    </div>
  );
}
