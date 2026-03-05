"""Integration tests: data fetch -> model -> charts pipeline."""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from models.dcf_model import DCFModel
from data.data_processor import DataProcessor
from charts import DCFCharts


def _mock_df(data):
    """Build a DataFrame mimicking yfinance's format (field names as index)."""
    return pd.DataFrame(data).T


class TestIntegration(unittest.TestCase):
    @patch("data.data_processor.yf.Ticker")
    def test_full_pipeline(self, mock_ticker_cls):
        """Fetch data, build model, run analyses, generate charts."""
        mock_stock = MagicMock()
        mock_ticker_cls.return_value = mock_stock

        mock_stock.info = {
            "trailingPE": 25.0,
            "enterpriseValue": 2e12,
            "totalDebt": 100e9,
            "totalCash": 50e9,
            "sharesOutstanding": 16e9,
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

        # data fetch
        params = DataProcessor().fetch_yahoo_data("AAPL")
        params.pop("current_price", None)  # not a model param

        # user-supplied inputs that aren't from Yahoo
        params["wacc"] = 0.08
        params["terminal_growth_rate"] = 0.02

        # model
        model = DCFModel(**params)
        iv = model.intrinsic_value(5)
        self.assertGreater(iv, 0)

        projections = model.project_cash_flows(5)
        sensitivity = model.sensitivity_analysis(5)
        scenarios = model.scenario_analysis(5)

        # basic structure checks
        self.assertIn("growth_rate", sensitivity)
        for name in ("Bear Case", "Base Case", "Bull Case"):
            self.assertIn(name, scenarios)

        # charts (just make sure they don't crash)
        c = DCFCharts()
        proj_img = c.create_projections_chart(projections)
        sens_img = c.create_sensitivity_chart(sensitivity)
        scen_img = c.create_scenarios_chart(scenarios)

        for img in (proj_img, sens_img, scen_img):
            self.assertIsInstance(img, str)
            self.assertGreater(len(img), 100)  # non-trivial base64

    def test_invalid_wacc_raises(self):
        model = DCFModel(
            enterprise_value=1000,
            debt=200,
            cash=100,
            shares_outstanding=10,
            last_fcf=50,
            growth_rate=0.05,
            wacc=0.01,
            terminal_growth_rate=0.02,
        )
        with self.assertRaises(ValueError):
            model.intrinsic_value(5)

    def test_zero_shares_returns_zero(self):
        model = DCFModel(
            enterprise_value=1000,
            debt=200,
            cash=100,
            shares_outstanding=0,
            last_fcf=50,
            growth_rate=0.05,
            wacc=0.08,
            terminal_growth_rate=0.02,
        )
        self.assertEqual(model.intrinsic_value(5), 0)

    def test_negative_fcf(self):
        model = DCFModel(
            enterprise_value=1000,
            debt=200,
            cash=100,
            shares_outstanding=10,
            last_fcf=-50,
            growth_rate=0.05,
            wacc=0.08,
            terminal_growth_rate=0.02,
        )
        result = model.intrinsic_value(5)
        self.assertIsInstance(result, (int, float))


if __name__ == "__main__":
    unittest.main()
