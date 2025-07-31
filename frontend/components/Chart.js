import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function ForexChart({ symbol }) {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: `${symbol} Price`,
        data: [],
        borderColor: '#D4A017', // Gold
        backgroundColor: 'rgba(212, 160, 23, 0.2)',
        fill: true,
      },
    ],
  });

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const res = await axios.get(`http://your-backend-api/chart/${symbol}`);
        setChartData({
          labels: res.data.labels, // Timestamps
          datasets: [
            {
              label: `${symbol} Price`,
              data: res.data.prices, // Close prices
              borderColor: '#D4A017',
              backgroundColor: 'rgba(212, 160, 23, 0.2)',
              fill: true,
            },
          ],
        });
      } catch (error) {
        console.error(`Error fetching chart data for ${symbol}:`, error);
      }
    };

    fetchChartData();
    const interval = setInterval(fetchChartData, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, [symbol]);

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true, labels: { color: '#D4A017' } },
      title: { display: true, text: `${symbol} Live Chart`, color: '#D4A017' },
    },
    scales: {
      x: { ticks: { color: '#FFFFFF' } },
      y: { ticks: { color: '#FFFFFF' } },
    },
  };

  return (
    <div className="p-4 bg-bamboo-green rounded-lg shadow-lg">
      <Line data={chartData} options={options} />
    </div>
  );
}
