import unittest
import pandas as pd
from stockpulse import fetch_stock_data, intra_day_data

class TestStockPulse(unittest.TestCase):
    def test_fetch_stock_data(self):
        data = fetch_stock_data(tickers=["AAPL"], save_to_csv=False)
        self.assertIn("AAPL", data)
        self.assertIsInstance(data["AAPL"], pd.DataFrame)
        self.assertTrue(all(col in data["AAPL"].columns for col in ["Open", "High", "Low", "Close", "Volume"]))

    def test_intra_day_data(self):
        data = intra_day_data(tickers=["AAPL"], period="1d", save_to_csv=False)
        self.assertIn("AAPL", data)
        self.assertIsInstance(data["AAPL"], pd.DataFrame)

if __name__ == "__main__":
    unittest.main()