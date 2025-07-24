"""
        Unit Tests for DCF Model Module

        Tests the core DCF calculation functionality including sensitivity and scenario analysis.
        """

        import unittest
        from models.dcf_model import DiscountedCashFlowModel

        class TestDiscountedCashFlowModel(unittest.TestCase):
            """Test suite for DiscountedCashFlowModel class"""

            def setUp(self):
                self.model = DiscountedCashFlowModel(
                    enterprise_value=1000,
                    debt=200,
                    cash=100,
                    shares_outstanding=10,
                    last_fcf=50,
                    growth_rate=0.05,
                    wacc=0.08,
                    terminal_growth_rate=0.02,
                    industry='Technology'
                )

            def test_calculate_equity_value(self):
                """Test the calculation of equity value"""
                self.assertEqual(self.model.calculate_equity_value(), 900)

            def test_calculate_implied_share_price(self):
                """Test the calculation of implied share price"""
                self.assertEqual(self.model.calculate_implied_share_price(), 90)

            def test_project_free_cash_flows(self):
                """Test the projection of free cash flows"""
                projected_fcf = self.model.project_free_cash_flows(3)
                self.assertEqual(len(projected_fcf), 3)
                self.assertAlmostEqual(projected_fcf[0], 52.5)

            def test_calculate_terminal_value(self):
                """Test the calculation of terminal value"""
                terminal_value = self.model.calculate_terminal_value(100)
                self.assertAlmostEqual(terminal_value, 1700)

            def test_calculate_present_value(self):
                """Test the calculation of present value"""
                cash_flows = [50, 52.5, 55.125]
                terminal_value = 2550
                pv = self.model.calculate_present_value(cash_flows, terminal_value)
                self.assertGreater(pv, 0)

            def test_sensitivity_analysis_structure(self):
                """Test that sensitivity analysis returns proper structure"""
                results = self.model.sensitivity_analysis(years=5)

                # Check that all expected variables are present
                expected_variables = ['growth_rate', 'wacc', 'terminal_growth_rate']
                for variable in expected_variables:
                    self.assertIn(variable, results)

                # Check that each variable has the expected number of scenarios
                for variable, scenarios in results.items():
                    self.assertEqual(len(scenarios), 5)  # Default range has 5 values

                    # Check each scenario has required fields
                    for scenario in scenarios:
                        self.assertIn('adjustment', scenario)
                        self.assertIn('intrinsic_value', scenario)
                        self.assertIn('percentage_change', scenario)

            def test_sensitivity_analysis_values(self):
                """Test that sensitivity analysis produces reasonable values"""
                results = self.model.sensitivity_analysis(years=5)

                # Test growth rate sensitivity
                growth_scenarios = results['growth_rate']
                base_case = next(s for s in growth_scenarios if s['adjustment'] == 0)
                positive_case = next(s for s in growth_scenarios if s['adjustment'] == 0.01)
                negative_case = next(s for s in growth_scenarios if s['adjustment'] == -0.01)

                # Higher growth should lead to higher valuation
                self.assertGreater(positive_case['intrinsic_value'], base_case['intrinsic_value'])
                self.assertLess(negative_case['intrinsic_value'], base_case['intrinsic_value'])

            def test_sensitivity_analysis_custom_ranges(self):
                """Test sensitivity analysis with custom variable ranges"""
                custom_ranges = {
                    'growth_rate': [-0.01, 0, 0.01],
                    'wacc': [-0.005, 0, 0.005]
                }
                results = self.model.sensitivity_analysis(years=5, variable_ranges=custom_ranges)

                self.assertEqual(len(results['growth_rate']), 3)
                self.assertEqual(len(results['wacc']), 3)
                self.assertNotIn('terminal_growth_rate', results)

            def test_scenario_analysis_structure(self):
                """Test that scenario analysis returns proper structure"""
                results = self.model.scenario_analysis(years=5)

                # Check that all expected scenarios are present
                expected_scenarios = ['Bear Case', 'Base Case', 'Bull Case']
                for scenario in expected_scenarios:
                    self.assertIn(scenario, results)

                # Check each scenario has required fields (assuming no errors)
                for scenario_name, scenario_data in results.items():
                    if 'error' not in scenario_data:
                        required_fields = ['intrinsic_value', 'upside_percentage', 'growth_rate', 'wacc', 'terminal_growth_rate']
                        for field in required_fields:
                            self.assertIn(field, scenario_data)

            def test_scenario_analysis_values(self):
                """Test that scenario analysis produces reasonable relative values"""
                results = self.model.scenario_analysis(years=5)

                # Assuming no errors in calculations
                if all('error' not in scenario for scenario in results.values()):
                    bear_value = results['Bear Case']['intrinsic_value']
                    base_value = results['Base Case']['intrinsic_value']
                    bull_value = results['Bull Case']['intrinsic_value']

                    # Bull case should be highest, bear case lowest
                    self.assertGreater(bull_value, base_value)
                    self.assertGreater(base_value, bear_value)

            def test_scenario_analysis_parameter_restoration(self):
                """Test that original parameters are restored after scenario analysis"""
                original_growth = self.model.growth_rate
                original_wacc = self.model.wacc
                original_terminal = self.model.terminal_growth_rate

                self.model.scenario_analysis(years=5)

                # Parameters should be restored to original values
                self.assertEqual(self.model.growth_rate, original_growth)
                self.assertEqual(self.model.wacc, original_wacc)
                self.assertEqual(self.model.terminal_growth_rate, original_terminal)

            def test_invalid_parameters_handling(self):
                """Test handling of invalid parameters (WACC <= terminal growth)"""
                # Create a model with WACC lower than terminal growth
                invalid_model = DiscountedCashFlowModel(
                    enterprise_value=1000, debt=200, cash=100, shares_outstanding=10,
                    last_fcf=50, growth_rate=0.05, wacc=0.01, terminal_growth_rate=0.02
                )

                with self.assertRaises(ValueError):
                    invalid_model.calculate_intrinsic_value(5)

            def test_zero_shares_outstanding(self):
                """Test handling of zero shares outstanding"""
                zero_shares_model = DiscountedCashFlowModel(
                    enterprise_value=1000, debt=200, cash=100, shares_outstanding=0,
                    last_fcf=50, growth_rate=0.05, wacc=0.08, terminal_growth_rate=0.02
                )

                self.assertEqual(zero_shares_model.calculate_implied_share_price(), 0)
                self.assertEqual(zero_shares_model.calculate_intrinsic_value(5), 0)

        if __name__ == "__main__":
            unittest.main()