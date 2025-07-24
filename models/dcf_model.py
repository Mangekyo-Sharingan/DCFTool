"""
Discounted Cash Flow Model - Core Valuation Logic

This module contains the DCF calculation engine for equity valuation.
"""
import numpy as np

class DiscountedCashFlowModel:
    """
    A comprehensive DCF model for equity valuation.

    This class implements the standard DCF methodology with configurable
    parameters for growth rates, discount rates, and projection periods.
    """

    def __init__(self, enterprise_value, debt, cash, shares_outstanding, last_fcf,
                 growth_rate, wacc, terminal_growth_rate, industry='N/A'):
        self.enterprise_value = enterprise_value
        self.debt = debt
        self.cash = cash
        self.shares_outstanding = shares_outstanding
        self.last_fcf = last_fcf
        self.growth_rate = growth_rate
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate
        self.industry = industry
#############
    def sensitivity_analysis(self, years=5, variable_ranges=None):
        """
        Performs sensitivity analysis on key DCF variables.

        Args:
            years: Projection period
            variable_ranges: Dict with variable names and their range adjustments

        Returns:
            Dict with sensitivity results for each variable
        """
        if variable_ranges is None:
            variable_ranges = {
                'growth_rate': [-0.02, -0.01, 0, 0.01, 0.02],  # +/- 2%
                'wacc': [-0.01, -0.005, 0, 0.005, 0.01],  # +/- 1%
                'terminal_growth_rate': [-0.005, -0.0025, 0, 0.0025, 0.005]  # +/- 0.5%
            }

        base_intrinsic_value = self.calculate_intrinsic_value(years)
        sensitivity_results = {}

        for variable, adjustments in variable_ranges.items():
            results = []
            original_value = getattr(self, variable)

            for adjustment in adjustments:
                # Temporarily adjust the variable
                setattr(self, variable, original_value + adjustment)
                try:
                    adjusted_value = self.calculate_intrinsic_value(years)
                    percentage_change = ((adjusted_value - base_intrinsic_value) / base_intrinsic_value) * 100
                    results.append({
                        'adjustment': adjustment,
                        'intrinsic_value': adjusted_value,
                        'percentage_change': percentage_change
                    })
                except ValueError:
                    # Handle cases where WACC <= terminal growth rate
                    results.append({
                        'adjustment': adjustment,
                        'intrinsic_value': 0,
                        'percentage_change': -100
                    })

            # Restore original value
            setattr(self, variable, original_value)
            sensitivity_results[variable] = results

        return sensitivity_results

    def scenario_analysis(self, years=5):
        """
        Performs scenario analysis with predefined bear/base/bull cases.

        Returns:
            Dict with results for each scenario
        """
        scenarios = {
            'Bear Case': {
                'growth_rate_adj': -0.02,  # 2% lower growth
                'wacc_adj': 0.01,  # 1% higher discount rate
                'terminal_growth_adj': -0.005  # 0.5% lower terminal growth
            },
            'Base Case': {
                'growth_rate_adj': 0,
                'wacc_adj': 0,
                'terminal_growth_adj': 0
            },
            'Bull Case': {
                'growth_rate_adj': 0.02,  # 2% higher growth
                'wacc_adj': -0.005,  # 0.5% lower discount rate
                'terminal_growth_adj': 0.005  # 0.5% higher terminal growth
            }
        }

        # Store original values
        original_growth = self.growth_rate
        original_wacc = self.wacc
        original_terminal = self.terminal_growth_rate

        scenario_results = {}

        for scenario_name, adjustments in scenarios.items():
            # Apply adjustments
            self.growth_rate = original_growth + adjustments['growth_rate_adj']
            self.wacc = original_wacc + adjustments['wacc_adj']
            self.terminal_growth_rate = original_terminal + adjustments['terminal_growth_adj']

            try:
                intrinsic_value = self.calculate_intrinsic_value(years)
                current_price = self.calculate_implied_share_price()
                upside = ((intrinsic_value - current_price) / current_price * 100) if current_price else 0

                scenario_results[scenario_name] = {
                    'intrinsic_value': intrinsic_value,
                    'upside_percentage': upside,
                    'growth_rate': self.growth_rate,
                    'wacc': self.wacc,
                    'terminal_growth_rate': self.terminal_growth_rate
                }
            except ValueError:
                scenario_results[scenario_name] = {
                    'intrinsic_value': 0,
                    'upside_percentage': -100,
                    'growth_rate': self.growth_rate,
                    'wacc': self.wacc,
                    'terminal_growth_rate': self.terminal_growth_rate,
                    'error': 'Invalid parameters (WACC <= Terminal Growth)'
                }

        # Restore original values
        self.growth_rate = original_growth
        self.wacc = original_wacc
        self.terminal_growth_rate = original_terminal

        return scenario_results
###########

    def calculate_equity_value(self):
        return self.enterprise_value - self.debt + self.cash

    def calculate_implied_share_price(self):
        equity_value = self.calculate_equity_value()
        return equity_value / self.shares_outstanding if self.shares_outstanding else 0

    def project_free_cash_flows(self, years=5):
        projected_fcf = []
        for year in range(1, years + 1):
            fcf = self.last_fcf * (1 + self.growth_rate) ** year
            projected_fcf.append(fcf)
        return projected_fcf

    def calculate_terminal_value(self, final_fcf):
        denominator = self.wacc - self.terminal_growth_rate
        if denominator <= 0:
            # Avoid division by zero or negative denominator
            raise ValueError("WACC must be greater than the terminal growth rate.")
        return (final_fcf * (1 + self.terminal_growth_rate)) / denominator

    def calculate_present_value(self, cash_flows, terminal_value):
        pv_fcf = sum(fcf / ((1 + self.wacc) ** (i + 1)) for i, fcf in enumerate(cash_flows))
        pv_terminal_value = terminal_value / ((1 + self.wacc) ** len(cash_flows))
        return pv_fcf + pv_terminal_value

    def calculate_intrinsic_value(self, years=5):
        # Industry-specific model switching can be implemented here.
        # For example:
        # if 'Financial' in self.industry:
        #     return self.some_other_model()
        projected_fcf = self.project_free_cash_flows(years)
        if not projected_fcf:
            return 0

        final_fcf = projected_fcf[-1]
        terminal_value = self.calculate_terminal_value(final_fcf)
        intrinsic_enterprise_value = self.calculate_present_value(projected_fcf, terminal_value)
        intrinsic_equity_value = intrinsic_enterprise_value - self.debt + self.cash

        return intrinsic_equity_value / self.shares_outstanding if self.shares_outstanding else 0
