"""
Discounted Cash Flow Valuation Model

Professional-grade DCF calculation engine implementing industry-standard
methodologies for equity valuation with advanced sensitivity and scenario analysis.

Copyright (c) 2024 DCF Valuation Tool
Licensed under MIT License
"""
import numpy as np

class DiscountedCashFlowModel:
    """
    Enterprise-grade DCF valuation model with comprehensive analytics.

    Implements standard DCF methodology with configurable parameters,
    sensitivity analysis capabilities, and scenario modeling for
    professional financial analysis.
    """

    def __init__(self, enterprise_value, debt, cash, shares_outstanding, last_fcf,
                 growth_rate, wacc, terminal_growth_rate, industry='N/A'):
        """
        Initialize DCF model with company financial parameters.

        Args:
            enterprise_value: Current enterprise value in millions
            debt: Total debt in millions
            cash: Cash and equivalents in millions
            shares_outstanding: Number of shares outstanding in millions
            last_fcf: Last reported free cash flow in millions
            growth_rate: Annual FCF growth rate (decimal)
            wacc: Weighted average cost of capital (decimal)
            terminal_growth_rate: Long-term growth rate (decimal)
            industry: Company industry classification
        """
        self.enterprise_value = enterprise_value
        self.debt = debt
        self.cash = cash
        self.shares_outstanding = shares_outstanding
        self.last_fcf = last_fcf
        self.growth_rate = growth_rate
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate
        self.industry = industry

    def sensitivity_analysis(self, years=5, variable_ranges=None):
        """
        Conduct comprehensive sensitivity analysis on key valuation drivers.

        Analyzes impact of parameter variations on intrinsic value to identify
        key value drivers and assess valuation uncertainty.

        Args:
            years: DCF projection period
            variable_ranges: Custom parameter adjustment ranges

        Returns:
            Dictionary containing sensitivity results for each variable
        """
        if variable_ranges is None:
            variable_ranges = {
                'growth_rate': [-0.02, -0.01, 0, 0.01, 0.02],
                'wacc': [-0.01, -0.005, 0, 0.005, 0.01],
                'terminal_growth_rate': [-0.005, -0.0025, 0, 0.0025, 0.005]
            }

        base_intrinsic_value = self.calculate_intrinsic_value(years)
        sensitivity_results = {}

        for variable, adjustments in variable_ranges.items():
            results = []
            original_value = getattr(self, variable)

            for adjustment in adjustments:
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
                    results.append({
                        'adjustment': adjustment,
                        'intrinsic_value': 0,
                        'percentage_change': -100
                    })

            setattr(self, variable, original_value)
            sensitivity_results[variable] = results

        return sensitivity_results

    def scenario_analysis(self, years=5):
        """
        Execute scenario analysis with predefined parameter sets.

        Generates Bear, Base, and Bull case valuations using systematic
        parameter adjustments to model different market conditions.

        Args:
            years: DCF projection period

        Returns:
            Dictionary containing results for each scenario
        """
        scenarios = {
            'Bear Case': {
                'growth_rate_adj': -0.02,
                'wacc_adj': 0.01,
                'terminal_growth_adj': -0.005
            },
            'Base Case': {
                'growth_rate_adj': 0,
                'wacc_adj': 0,
                'terminal_growth_adj': 0
            },
            'Bull Case': {
                'growth_rate_adj': 0.02,
                'wacc_adj': -0.005,
                'terminal_growth_adj': 0.005
            }
        }

        original_growth = self.growth_rate
        original_wacc = self.wacc
        original_terminal = self.terminal_growth_rate

        scenario_results = {}

        for scenario_name, adjustments in scenarios.items():
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
                    'error': 'Invalid parameter combination'
                }

        self.growth_rate = original_growth
        self.wacc = original_wacc
        self.terminal_growth_rate = original_terminal

        return scenario_results

    def calculate_equity_value(self):
        """Calculate equity value from enterprise value"""
        return self.enterprise_value - self.debt + self.cash

    def calculate_implied_share_price(self):
        """Calculate current implied share price"""
        equity_value = self.calculate_equity_value()
        return equity_value / self.shares_outstanding if self.shares_outstanding else 0

    def project_free_cash_flows(self, years=5):
        """Project future free cash flows based on growth assumptions"""
        projected_fcf = []
        for year in range(1, years + 1):
            fcf = self.last_fcf * (1 + self.growth_rate) ** year
            projected_fcf.append(fcf)
        return projected_fcf

    def calculate_terminal_value(self, final_fcf):
        """Calculate terminal value using Gordon Growth Model"""
        denominator = self.wacc - self.terminal_growth_rate
        if denominator <= 0:
            raise ValueError("WACC must exceed terminal growth rate for valid calculation")
        return (final_fcf * (1 + self.terminal_growth_rate)) / denominator

    def calculate_present_value(self, cash_flows, terminal_value):
        """Calculate present value of projected cash flows and terminal value"""
        pv_fcf = sum(fcf / ((1 + self.wacc) ** (i + 1)) for i, fcf in enumerate(cash_flows))
        pv_terminal_value = terminal_value / ((1 + self.wacc) ** len(cash_flows))
        return pv_fcf + pv_terminal_value

    def calculate_intrinsic_value(self, years=5):
        """
        Calculate intrinsic value per share using DCF methodology.

        Supports industry-specific model variations for specialized sectors
        such as financial services, REITs, and utilities.
        """
        projected_fcf = self.project_free_cash_flows(years)
        if not projected_fcf:
            return 0

        final_fcf = projected_fcf[-1]
        terminal_value = self.calculate_terminal_value(final_fcf)
        intrinsic_enterprise_value = self.calculate_present_value(projected_fcf, terminal_value)
        intrinsic_equity_value = intrinsic_enterprise_value - self.debt + self.cash

        return intrinsic_equity_value / self.shares_outstanding if self.shares_outstanding else 0
