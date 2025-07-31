import React from "react";
import Footer from "../components/Footer";

export default function Dashboard() {
  return (
    <div>
      <div style={{ backgroundColor: 'green', padding: '10px' }}>
        <h1 style={{ color: 'gold' }}>Elite Trading</h1>
        <nav>
          <a href="/">Dashboard</a>
          <a href="/trades">Trades</a>
          <a href="/history">History</a>
          <a href="/balance">Balance</a>
        </nav>
      </div>

      <h2 style={{ color: 'gold' }}>Trading Dashboard</h2>

      <div style={{ backgroundColor: 'green', padding: '10px', margin: '10px 0' }}>
        <h3>Balance</h3>
        <p>$0.00</p>
      </div>

      <div style={{ backgroundColor: 'green', padding: '10px', margin: '10px 0' }}>
        <h3>Equity</h3>
        <p>$0.00</p>
      </div>

      <div style={{ backgroundColor: 'green', padding: '10px', margin: '10px 0' }}>
        <h3>Profit/Loss</h3>
        <p>$0.00</p>
      </div>

      <div>
        <h3 style={{ color: 'gold' }}>Recent Trades</h3>
        <table>
          <thead>
            <tr style={{ backgroundColor: 'green', color: 'white' }}>
              <th>Symbol</th>
              <th>Action</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {/* Recent trades rows go here */}
          </tbody>
        </table>
        <a href="/trades">View All Trades</a>
      </div>

      <Footer />
    </div>
  );
  }
