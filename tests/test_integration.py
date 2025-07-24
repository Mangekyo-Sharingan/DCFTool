"""
Integration Tests for DCF Tool

Tests the complete workflow from data fetching to chart generation.
"""

import pandas as pd
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gui.app_window import DCFAnalyzerApp
from models.dcf_model import DiscountedCashFlowModel
from data.data_processor import DataProcessor

class TestDCFIntegration(unittest.TestCase):
    """Integration test suite for the complete DCF workflow"""

    def setUp(self):
        """Set up integration test environment"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing

    def tearDown(self):
        """Clean up after integration tests"""
        self.root.destroy()

    @patch('data.data_processor.yf.Ticker')
    def test_complete_dcf_workflow(self, mock_ticker):
        """Test the complete workflow from data fetch to DCF calculation"""
        # Mock yfinance data
        mock_stock = MagicMock()
        mock_ticker.return_value = mock_stock

        mock_stock.info = {
            'trailingPE': 25.0,
            'enterpriseValue': 2000000000000,
            'totalDebt': 100000000000,
            'totalCash': 50000000000,
            'sharesOutstanding': 16000000000,
            'industry': 'Technology'
        }

        mock_financials = pd.DataFrame({
            'Total Revenue': [365000000000, 350000000000, 340000000000]
        })
        mock_cash_flow = pd.DataFrame({
            'Total Cash From Operating Activities': [100000000000],
            'Capital Expenditures': [-20000000000]
        })

        mock_stock.financials = mock_financials
        mock_stock.balance_sheet = pd.DataFrame()
        mock_stock.cashflow = mock_cash_flow

        # Test data processor
        processor = DataProcessor()
        params = processor.fetch_yahoo_data("AAPL")

        # Test DCF model creation and calculation
        model = DiscountedCashFlowModel(**params)
        intrinsic_value = model.calculate_intrinsic_value(5)

        # Verify reasonable results
        self.assertGreater(intrinsic_value, 0)
        self.assertIsInstance(intrinsic_value, (int, float))

        # Test sensitivity analysis
        sensitivity_results = model.sensitivity_analysis(5)
        self.assertIn('growth_rate', sensitivity_results)
        self.assertIn('wacc', sensitivity_results)
        self.assertIn('terminal_growth_rate', sensitivity_results)

        # Test scenario analysis
        scenario_results = model.scenario_analysis(5)
        expected_scenarios = ['Bear Case', 'Base Case', 'Bull Case']
        for scenario in expected_scenarios:
            self.assertIn(scenario, scenario_results)

    def test_model_parameter_validation(self):
        """Test that the DCF model properly validates parameters"""
        # Test with invalid parameters (WACC <= terminal growth)
        with self.assertRaises(ValueError):
            model = DiscountedCashFlowModel(
                enterprise_value=1000, debt=200, cash=100, shares_outstanding=10,
                last_fcf=50, growth_rate=0.05, wacc=0.01, terminal_growth_rate=0.02
            )
            model.calculate_intrinsic_value(5)

    def test_edge_case_handling(self):
        """Test handling of edge cases in calculations"""
        # Test with zero shares outstanding
        model = DiscountedCashFlowModel(
            enterprise_value=1000, debt=200, cash=100, shares_outstanding=0,
            last_fcf=50, growth_rate=0.05, wacc=0.08, terminal_growth_rate=0.02
        )

        intrinsic_value = model.calculate_intrinsic_value(5)
        self.assertEqual(intrinsic_value, 0)

        # Test with negative FCF
        model_neg_fcf = DiscountedCashFlowModel(
            enterprise_value=1000, debt=200, cash=100, shares_outstanding=10,
            last_fcf=-50, growth_rate=0.05, wacc=0.08, terminal_growth_rate=0.02
        )

        # Should still calculate (though result may be negative)
        result = model_neg_fcf.calculate_intrinsic_value(5)
        self.assertIsInstance(result, (int, float))

    @patch('gui.app_window.DCFCharts')
    def test_chart_integration(self, mock_charts):
        """Test integration between DCF calculations and chart generation"""
        mock_chart_instance = MagicMock()
        mock_charts.return_value = mock_chart_instance

        # Mock chart methods to return mock canvas objects
        mock_canvas = MagicMock()
        mock_canvas.get_tk_widget.return_value = MagicMock()

        mock_chart_instance.create_cash_flow_chart.return_value = mock_canvas
        mock_chart_instance.create_sensitivity_chart.return_value = mock_canvas
        mock_chart_instance.create_scenario_chart.return_value = mock_canvas

        # Create model with valid parameters
        model = DiscountedCashFlowModel(
            enterprise_value=1000, debt=200, cash=100, shares_outstanding=10,
            last_fcf=50, growth_rate=0.05, wacc=0.08, terminal_growth_rate=0.02
        )

        # Simulate the chart update process
        projected_fcf = model.project_free_cash_flows(5)
        terminal_value = model.calculate_terminal_value(projected_fcf[-1])
        sensitivity_results = model.sensitivity_analysis(5)
        scenario_results = model.scenario_analysis(5)

        # Verify data structures are compatible with chart methods
        self.assertIsInstance(projected_fcf, list)
        self.assertGreater(len(projected_fcf), 0)
        self.assertIsInstance(terminal_value, (int, float))
        self.assertIsInstance(sensitivity_results, dict)
        self.assertIsInstance(scenario_results, dict)

if __name__ == "__main__":
    unittest.main()