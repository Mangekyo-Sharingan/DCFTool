# test_dcf_model.py

import unittest
from models.dcf_model import DiscountedCashFlowModel

class TestDiscountedCashFlowModel(unittest.TestCase):
    def setUp(self):
        self.model = DiscountedCashFlowModel(
            enterprise_value=1000,
            debt=200,
            cash=100,
            shares_outstanding=10,
            last_fcf=50,
            growth_rate=0.05,
            wacc=0.08,
            terminal_growth_rate=0.02
        )

    def test_calculate_equity_value(self):
        self.assertEqual(self.model.calculate_equity_value(), 900)

    def test_calculate_implied_share_price(self):
        self.assertEqual(self.model.calculate_implied_share_price(), 90)

    def test_project_free_cash_flows(self):
        projected_fcf = self.model.project_free_cash_flows(3)
        self.assertEqual(len(projected_fcf), 3)
        self.assertAlmostEqual(projected_fcf[0], 52.5)

    def test_calculate_terminal_value(self):
        terminal_value = self.model.calculate_terminal_value(100)
        self.assertAlmostEqual(terminal_value, 1700)

    def test_calculate_present_value(self):
        cash_flows = [50, 52.5, 55.125]
        terminal_value = 2550
        pv = self.model.calculate_present_value(cash_flows, terminal_value)
        self.assertGreater(pv, 0)

if __name__ == "__main__":
    unittest.main()