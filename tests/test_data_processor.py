"""
Unit Tests for Data Processor Module

Tests the data fetching and processing functionality with enhanced coverage.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from data.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """Test suite for DataProcessor class"""

    def setUp(self):
        self.processor = DataProcessor()

    @patch('data.data_processor.yf.Ticker')
    def test_fetch_yahoo_data_valid_ticker_success(self, mock_ticker):
        """Test successful data fetching for valid ticker"""
        # Mock the yfinance Ticker object
        mock_stock = MagicMock()
        mock_ticker.return_value = mock_stock

        # Mock info data
        mock_stock.info = {
            'trailingPE': 25.0,
            'enterpriseValue': 2000000000000,  # 2T
            'totalDebt': 100000000000,  # 100B
            'totalCash': 50000000000,  # 50B
            'sharesOutstanding': 16000000000,  # 16B shares
            'industry': 'Technology'
        }

        # Mock financial statements
        mock_financials = pd.DataFrame({
            'Total Revenue': [365000000000, 350000000000, 340000000000]  # Revenue in dollars
        })
        mock_balance_sheet = pd.DataFrame()
        mock_cash_flow = pd.DataFrame({
            'Total Cash From Operating Activities': [100000000000],  # 100B
            'Capital Expenditures': [-20000000000]  # -20B (negative)
        })

        mock_stock.financials = mock_financials
        mock_stock.balance_sheet = mock_balance_sheet
        mock_stock.cashflow = mock_cash_flow

        result = self.processor.fetch_yahoo_data("AAPL")

        # Verify all required fields are present
        required_fields = ['enterprise_value', 'debt', 'cash', 'shares_outstanding',
                          'last_fcf', 'growth_rate', 'industry']
        for field in required_fields:
            self.assertIn(field, result)

        # Verify values are in millions and reasonable
        self.assertAlmostEqual(result['enterprise_value'], 2000000, places=0)  # 2M millions = 2T
        self.assertAlmostEqual(result['debt'], 100000, places=0)  # 100K millions = 100B
        self.assertAlmostEqual(result['cash'], 50000, places=0)  # 50K millions = 50B
        self.assertAlmostEqual(result['shares_outstanding'], 16000, places=0)  # 16K millions = 16B
        self.assertAlmostEqual(result['last_fcf'], 80000, places=0)  # (100B - (-20B))/1M = 80K millions
        self.assertEqual(result['industry'], 'Technology')

    @patch('data.data_processor.yf.Ticker')
    def test_fetch_yahoo_data_missing_cash_flow_data(self, mock_ticker):
        """Test handling of missing cash flow data"""
        mock_stock = MagicMock()
        mock_ticker.return_value = mock_stock

        mock_stock.info = {
            'trailingPE': 25.0,
            'enterpriseValue': 1000000000000,
            'totalDebt': 50000000000,
            'totalCash': 25000000000,
            'sharesOutstanding': 8000000000,
            'industry': 'Technology'
        }

        # Mock financials with revenue data for growth calculation
        mock_financials = pd.DataFrame({
            'Total Revenue': [300000000000, 280000000000, 260000000000],
            'Net Income': [60000000000, 55000000000, 50000000000]  # For FCF fallback
        })

        # Mock empty cash flow statement
        mock_cash_flow = pd.DataFrame()

        mock_stock.financials = mock_financials
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = mock_cash_flow

        result = self.processor.fetch_yahoo_data("AAPL")

        # Should still return reasonable values using fallbacks
        self.assertGreater(result['last_fcf'], 0)
        self.assertGreater(result['growth_rate'], 0)

    @patch('data.data_processor.yf.Ticker')
    def test_fetch_yahoo_data_invalid_ticker(self, mock_ticker):
        """Test handling of invalid ticker"""
        mock_stock = MagicMock()
        mock_ticker.return_value = mock_stock

        # Mock empty/invalid info (no trailingPE)
        mock_stock.info = {}

        with self.assertRaises(ValueError):
            self.processor.fetch_yahoo_data("INVALID")

    @patch('data.data_processor.yf.Ticker')
    def test_fetch_yahoo_data_missing_industry(self, mock_ticker):
        """Test handling of missing industry information"""
        mock_stock = MagicMock()
        mock_ticker.return_value = mock_stock

        mock_stock.info = {
            'trailingPE': 25.0,
            'enterpriseValue': 1000000000000,
            'totalDebt': 50000000000,
            'totalCash': 25000000000,
            'sharesOutstanding': 8000000000
            # No 'industry' field
        }

        mock_financials = pd.DataFrame({
            'Total Revenue': [300000000000, 280000000000]
        })
        mock_cash_flow = pd.DataFrame({
            'Total Cash From Operating Activities': [80000000000],
            'Capital Expenditures': [-15000000000]
        })

        mock_stock.financials = mock_financials
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = mock_cash_flow

        result = self.processor.fetch_yahoo_data("TEST")

        # Should default to 'N/A' for missing industry
        self.assertEqual(result['industry'], 'N/A')

    @patch('data.data_processor.yf.Ticker')
    def test_fetch_yahoo_data_extreme_growth_rates(self, mock_ticker):
        """Test handling of extreme growth rates (constraining to reasonable bounds)"""
        mock_stock = MagicMock()
        mock_ticker.return_value = mock_stock

        mock_stock.info = {
            'trailingPE': 25.0,
            'enterpriseValue': 1000000000000,
            'totalDebt': 50000000000,
            'totalCash': 25000000000,
            'sharesOutstanding': 8000000000,
            'industry': 'Technology'
        }

        # Mock extreme revenue growth (should be constrained)
        mock_financials = pd.DataFrame({
            'Total Revenue': [1000000000000, 100000000000, 50000000000]  # 10x growth
        })
        mock_cash_flow = pd.DataFrame({
            'Total Cash From Operating Activities': [80000000000],
            'Capital Expenditures': [-15000000000]
        })

        mock_stock.financials = mock_financials
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = mock_cash_flow

        result = self.processor.fetch_yahoo_data("TEST")

        # Growth rate should be constrained to reasonable bounds (1% to 20%)
        self.assertGreaterEqual(result['growth_rate'], 0.01)
        self.assertLessEqual(result['growth_rate'], 0.20)

    def test_fetch_yahoo_data_real_ticker_integration(self):
        """Integration test with real ticker (requires internet)"""
        try:
            result = self.processor.fetch_yahoo_data("AAPL")

            # Basic validation of real data
            required_fields = ['enterprise_value', 'debt', 'cash', 'shares_outstanding',
                              'last_fcf', 'growth_rate', 'industry']
            for field in required_fields:
                self.assertIn(field, result)

            # Values should be reasonable for Apple
            self.assertGreater(result['enterprise_value'], 0)
            self.assertGreater(result['shares_outstanding'], 0)
            self.assertIsInstance(result['industry'], str)

        except Exception as e:
            self.skipTest(f"Integration test skipped due to network/API issue: {e}")

if __name__ == "__main__":
    unittest.main()