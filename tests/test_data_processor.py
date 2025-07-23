# test_data_processor.py

import unittest
from data.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    def test_fetch_yahoo_data_valid_ticker(self):
        params = self.processor.fetch_yahoo_data("AAPL")
        self.assertIn("enterprise_value", params)
        self.assertIn("debt", params)
        self.assertIn("cash", params)
        self.assertIn("shares_outstanding", params)
        self.assertIn("last_fcf", params)
        self.assertIn("growth_rate", params)
        self.assertIn("industry", params)

    def test_fetch_yahoo_data_invalid_ticker(self):
        with self.assertRaises(ValueError):
            self.processor.fetch_yahoo_data("INVALID")

if __name__ == "__main__":
    unittest.main()