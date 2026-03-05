"""Tests for models.dcf_model"""

import unittest
from models.dcf_model import DCFModel


class TestDCFModel(unittest.TestCase):
    def setUp(self):
        self.model = DCFModel(
            enterprise_value=1000,
            debt=200,
            cash=100,
            shares_outstanding=10,
            last_fcf=50,
            growth_rate=0.05,
            wacc=0.08,
            terminal_growth_rate=0.02,
            industry="Technology",
        )

    # --- basic helpers ---

    def test_implied_share_price(self):
        # equity = 1000 - 200 + 100 = 900; 900/10 = 90
        self.assertEqual(self.model.implied_share_price(), 90)

    def test_project_free_cash_flows(self):
        projected = self.model.project_free_cash_flows(3)
        self.assertEqual(len(projected), 3)
        self.assertAlmostEqual(projected[0], 52.5)

    def test_calculate_terminal_value(self):
        # TV = 100*(1.02) / (0.08-0.02) = 102/0.06 = 1700
        tv = self.model.calculate_terminal_value(100)
        self.assertAlmostEqual(tv, 1700)

    def test_calculate_present_value(self):
        flows = [50, 52.5, 55.125]
        tv = 2550
        pv = self.model.calculate_present_value(flows, tv)
        self.assertGreater(pv, 0)

    # --- full valuation ---

    def test_intrinsic_value_positive(self):
        iv = self.model.intrinsic_value(5)
        self.assertGreater(iv, 0)

    def test_project_cash_flows_dict(self):
        result = self.model.project_cash_flows(5)
        for key in (
            "projected_fcf",
            "present_values",
            "terminal_value",
            "years",
            "wacc",
            "growth_rate",
            "terminal_growth_rate",
        ):
            self.assertIn(key, result)

    # --- sensitivity analysis ---

    def test_sensitivity_structure(self):
        results = self.model.sensitivity_analysis(5)
        for var in ("growth_rate", "wacc", "terminal_growth_rate"):
            self.assertIn(var, results)
            self.assertEqual(len(results[var]), 5)
            for entry in results[var]:
                self.assertIn("adjustment", entry)
                self.assertIn("intrinsic_value", entry)
                self.assertIn("percentage_change", entry)

    def test_sensitivity_direction(self):
        results = self.model.sensitivity_analysis(5)
        gr = results["growth_rate"]
        base = next(r for r in gr if r["adjustment"] == 0)
        up = next(r for r in gr if r["adjustment"] == 0.01)
        down = next(r for r in gr if r["adjustment"] == -0.01)
        self.assertGreater(up["intrinsic_value"], base["intrinsic_value"])
        self.assertLess(down["intrinsic_value"], base["intrinsic_value"])

    def test_sensitivity_custom_ranges(self):
        custom = {
            "growth_rate": [-0.01, 0, 0.01],
            "wacc": [-0.005, 0, 0.005],
        }
        results = self.model.sensitivity_analysis(5, variable_ranges=custom)
        self.assertEqual(len(results["growth_rate"]), 3)
        self.assertEqual(len(results["wacc"]), 3)
        self.assertNotIn("terminal_growth_rate", results)

    # --- scenario analysis ---

    def test_scenario_structure(self):
        results = self.model.scenario_analysis(5)
        for name in ("Bear Case", "Base Case", "Bull Case"):
            self.assertIn(name, results)
            if "error" not in results[name]:
                for key in (
                    "intrinsic_value",
                    "upside_percentage",
                    "growth_rate",
                    "wacc",
                    "terminal_growth_rate",
                ):
                    self.assertIn(key, results[name])

    def test_scenario_ordering(self):
        results = self.model.scenario_analysis(5)
        if all("error" not in r for r in results.values()):
            bear = results["Bear Case"]["intrinsic_value"]
            base = results["Base Case"]["intrinsic_value"]
            bull = results["Bull Case"]["intrinsic_value"]
            self.assertGreater(bull, base)
            self.assertGreater(base, bear)

    def test_scenario_restores_params(self):
        orig_gr = self.model.growth_rate
        orig_wacc = self.model.wacc
        orig_tg = self.model.terminal_growth_rate
        self.model.scenario_analysis(5)
        self.assertEqual(self.model.growth_rate, orig_gr)
        self.assertEqual(self.model.wacc, orig_wacc)
        self.assertEqual(self.model.terminal_growth_rate, orig_tg)

    # --- edge cases ---

    def test_wacc_below_terminal_growth_raises(self):
        bad = DCFModel(
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
            bad.intrinsic_value(5)

    def test_zero_shares(self):
        m = DCFModel(
            enterprise_value=1000,
            debt=200,
            cash=100,
            shares_outstanding=0,
            last_fcf=50,
            growth_rate=0.05,
            wacc=0.08,
            terminal_growth_rate=0.02,
        )
        self.assertEqual(m.implied_share_price(), 0)
        self.assertEqual(m.intrinsic_value(5), 0)


if __name__ == "__main__":
    unittest.main()
