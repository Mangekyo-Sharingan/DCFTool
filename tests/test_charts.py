"""
Unit Tests for Charts Module

Tests the chart generation functionality for DCF analysis visualization.
"""

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gui.charts import DCFCharts

class TestDCFCharts(unittest.TestCase):
    """Test suite for DCFCharts class"""

    def setUp(self):
        """Set up test fixtures"""
        self.charts = DCFCharts()
        self.root = tk.Tk()
        self.parent_frame = tk.Frame(self.root)

    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()

    @patch('gui.charts.FigureCanvasTkAgg')
    @patch('gui.charts.Figure')
    def test_create_cash_flow_chart(self, mock_figure, mock_canvas):
        """Test cash flow chart creation"""
        # Mock the figure and canvas
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_figure.return_value = mock_fig
        mock_fig.add_subplot.return_value = mock_ax

        projected_fcf = [100, 105, 110, 115, 120]
        terminal_value = 2000
        wacc = 0.08
        years = 5

        result = self.charts.create_cash_flow_chart(
            self.parent_frame, projected_fcf, terminal_value, wacc, years
        )

        # Verify figure was created with correct parameters
        mock_figure.assert_called_once()
        mock_fig.add_subplot.assert_called_once_with(111, facecolor='#2b2b2b')

        # Verify bars were created
        self.assertEqual(mock_ax.bar.call_count, 2)  # Two sets of bars

        # Verify canvas was created
        mock_canvas.assert_called_once_with(mock_fig, self.parent_frame)

    @patch('gui.charts.FigureCanvasTkAgg')
    @patch('gui.charts.Figure')
    def test_create_sensitivity_chart(self, mock_figure, mock_canvas):
        """Test sensitivity analysis tornado chart creation"""
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_figure.return_value = mock_fig
        mock_fig.add_subplot.return_value = mock_ax

        sensitivity_results = {
            'growth_rate': [
                {'adjustment': -0.01, 'intrinsic_value': 90, 'percentage_change': -10},
                {'adjustment': 0, 'intrinsic_value': 100, 'percentage_change': 0},
                {'adjustment': 0.01, 'intrinsic_value': 110, 'percentage_change': 10}
            ],
            'wacc': [
                {'adjustment': -0.005, 'intrinsic_value': 105, 'percentage_change': 5},
                {'adjustment': 0, 'intrinsic_value': 100, 'percentage_change': 0},
                {'adjustment': 0.005, 'intrinsic_value': 95, 'percentage_change': -5}
            ]
        }

        result = self.charts.create_sensitivity_chart(
            self.parent_frame, sensitivity_results
        )

        # Verify figure was created
        mock_figure.assert_called_once()
        mock_fig.add_subplot.assert_called_once()

        # Verify horizontal bars were created
        self.assertEqual(mock_ax.barh.call_count, 2)  # Two sets of horizontal bars

        # Verify canvas was created
        mock_canvas.assert_called_once()

    @patch('gui.charts.FigureCanvasTkAgg')
    @patch('gui.charts.Figure')
    def test_create_scenario_chart(self, mock_figure, mock_canvas):
        """Test scenario analysis chart creation"""
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_figure.return_value = mock_fig
        mock_fig.add_subplot.return_value = mock_ax

        scenario_results = {
            'Bear Case': {
                'intrinsic_value': 85,
                'upside_percentage': -15,
                'growth_rate': 0.03,
                'wacc': 0.09,
                'terminal_growth_rate': 0.015
            },
            'Base Case': {
                'intrinsic_value': 100,
                'upside_percentage': 0,
                'growth_rate': 0.05,
                'wacc': 0.08,
                'terminal_growth_rate': 0.02
            },
            'Bull Case': {
                'intrinsic_value': 120,
                'upside_percentage': 20,
                'growth_rate': 0.07,
                'wacc': 0.075,
                'terminal_growth_rate': 0.025
            }
        }

        result = self.charts.create_scenario_chart(
            self.parent_frame, scenario_results
        )

        # Verify figure was created
        mock_figure.assert_called_once()
        mock_fig.add_subplot.assert_called_once()

        # Verify bars were created
        mock_ax.bar.assert_called_once()

        # Verify canvas was created
        mock_canvas.assert_called_once()

    def test_scenario_chart_with_errors(self):
        """Test scenario chart handling of error cases"""
        scenario_results = {
            'Bear Case': {
                'error': 'Invalid parameters',
                'growth_rate': 0.03,
                'wacc': 0.01,  # WACC < terminal growth
                'terminal_growth_rate': 0.02
            },
            'Base Case': {
                'intrinsic_value': 100,
                'upside_percentage': 0,
                'growth_rate': 0.05,
                'wacc': 0.08,
                'terminal_growth_rate': 0.02
            }
        }

        # Should not raise an exception even with error scenarios
        try:
            result = self.charts.create_scenario_chart(
                self.parent_frame, scenario_results
            )
        except Exception as e:
            self.fail(f"create_scenario_chart raised {e} unexpectedly!")

    def test_empty_sensitivity_results(self):
        """Test handling of empty sensitivity results"""
        empty_results = {}

        try:
            result = self.charts.create_sensitivity_chart(
                self.parent_frame, empty_results
            )
        except Exception as e:
            self.fail(f"create_sensitivity_chart raised {e} with empty results!")

if __name__ == "__main__":
    unittest.main()