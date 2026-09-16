"""Tests for data.data_processor"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from data.data_processor import DataProcessor


def _mock_df(data):
    """Build a DataFrame mimicking yfinance's format (field names as index)."""
    return pd.DataFrame(data).T


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.proc = DataProcessor()

    @patch("data.data_processor.yf.Ticker")
    def test_valid_ticker(self, mock_ticker_cls):
        mock_stock = MagicMock()
        mock_ticker_cls.return_value = mock_stock

        mock_stock.info = {
            "trailingPE": 25.0,
            "enterpriseValue": 2_000_000_000_000,
            "totalDebt": 100_000_000_000,
            "totalCash": 50_000_000_000,
            "sharesOutstanding": 16_000_000_000,
            "industry": "Technology",
        }
        mock_stock.financials = _mock_df(
            {
                "Total Revenue": [365e9, 350e9, 340e9],
            }
        )
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = _mock_df(
            {
                "Total Cash From Operating Activities": [100e9],
                "Capital Expenditures": [-20e9],
            }
        )

        result = self.proc.fetch_yahoo_data("AAPL")

        for field in (
            "enterprise_value",
            "debt",
            "cash",
            "shares_outstanding",
            "last_fcf",
            "growth_rate",
            "industry",
        ):
            self.assertIn(field, result)

        self.assertAlmostEqual(result["enterprise_value"], 2_000_000, places=0)
        self.assertAlmostEqual(result["debt"], 100_000, places=0)
        self.assertAlmostEqual(result["last_fcf"], 80_000, places=0)
        self.assertEqual(result["industry"], "Technology")

    @patch("data.data_processor.yf.Ticker")
    def test_missing_cash_flow_uses_fallback(self, mock_ticker_cls):
        mock_stock = MagicMock()
        mock_ticker_cls.return_value = mock_stock

        mock_stock.info = {
            "trailingPE": 25.0,
            "enterpriseValue": 1e12,
            "totalDebt": 50e9,
            "totalCash": 25e9,
            "sharesOutstanding": 8e9,
            "industry": "Technology",
        }
        mock_stock.financials = _mock_df(
            {
                "Total Revenue": [300e9, 280e9, 260e9],
                "Net Income": [60e9, 55e9, 50e9],
            }
        )
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = pd.DataFrame()  # empty -- triggers fallback

        result = self.proc.fetch_yahoo_data("AAPL")
        self.assertGreater(result["last_fcf"], 0)
        self.assertGreater(result["growth_rate"], 0)

    @patch("data.data_processor.yf.Ticker")
    def test_invalid_ticker_raises(self, mock_ticker_cls):
        mock_stock = MagicMock()
        mock_ticker_cls.return_value = mock_stock
        mock_stock.info = {}

        with self.assertRaises(ValueError):
            self.proc.fetch_yahoo_data("INVALID")

    @patch("data.data_processor.yf.Ticker")
    def test_missing_industry_defaults(self, mock_ticker_cls):
        mock_stock = MagicMock()
        mock_ticker_cls.return_value = mock_stock

        mock_stock.info = {
            "trailingPE": 25.0,
            "enterpriseValue": 1e12,
            "totalDebt": 50e9,
            "totalCash": 25e9,
            "sharesOutstanding": 8e9,
        }
        mock_stock.financials = _mock_df(
            {
                "Total Revenue": [300e9, 280e9],
            }
        )
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = _mock_df(
            {
                "Total Cash From Operating Activities": [80e9],
                "Capital Expenditures": [-15e9],
            }
        )

        result = self.proc.fetch_yahoo_data("TEST")
        self.assertEqual(result["industry"], "N/A")

    @patch("data.data_processor.yf.Ticker")
    def test_extreme_growth_is_clamped(self, mock_ticker_cls):
        mock_stock = MagicMock()
        mock_ticker_cls.return_value = mock_stock

        mock_stock.info = {
            "trailingPE": 25.0,
            "enterpriseValue": 1e12,
            "totalDebt": 50e9,
            "totalCash": 25e9,
            "sharesOutstanding": 8e9,
            "industry": "Technology",
        }
        mock_stock.financials = _mock_df(
            {
                "Total Revenue": [1e12, 100e9, 50e9],
            }
        )
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = _mock_df(
            {
                "Total Cash From Operating Activities": [80e9],
                "Capital Expenditures": [-15e9],
            }
        )

        result = self.proc.fetch_yahoo_data("TEST")
        self.assertGreaterEqual(result["growth_rate"], -0.20)
        self.assertLessEqual(result["growth_rate"], 0.50)


if __name__ == "__main__":
    unittest.main()
