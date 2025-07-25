"""
Professional Financial Visualization Suite

Advanced charting and visualization components for DCF analysis including
cash flow projections, sensitivity analysis, and scenario modeling charts.

Copyright (c) 2024 DCF Valuation Tool
Licensed under MIT License
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import seaborn as sns


class DCFCharts:
    """
    Professional-grade financial charting system for DCF analysis.

    Provides comprehensive visualization capabilities including cash flow
    projections, sensitivity tornado charts, and scenario comparison analysis
    with publication-quality styling and formatting.
    """

    def __init__(self):
        """Initialize charting system with professional styling configuration"""
        plt.style.use('dark_background')
        sns.set_palette("husl")

    def create_cash_flow_chart(self, parent, projected_fcf, terminal_value, wacc, years):
        """
        Generate professional cash flow projection visualization.

        Creates comparative bar chart showing projected future cash flows
        alongside their present values with detailed value annotations
        and professional styling.

        Args:
            parent: Tkinter parent container widget
            projected_fcf: List of projected free cash flows
            terminal_value: Calculated terminal value
            wacc: Weighted average cost of capital
            years: Number of projection years

        Returns:
            FigureCanvasTkAgg: Embedded chart canvas for GUI integration
        """
        fig = Figure(figsize=(10, 6), facecolor='#1c1c1c')
        ax = fig.add_subplot(111, facecolor='#2b2b2b')

        # Calculate present values
        pv_fcf = [fcf / ((1 + wacc) ** (i + 1)) for i, fcf in enumerate(projected_fcf)]
        pv_terminal = terminal_value / ((1 + wacc) ** years)

        # Years for x-axis
        x_years = list(range(1, years + 1))
        x_years.append(f"Terminal")

        # Combine FCF and terminal value for display
        all_fcf = projected_fcf + [terminal_value]
        all_pv = pv_fcf + [pv_terminal]

        # Create bars
        bar_width = 0.35
        x_pos = np.arange(len(x_years))

        bars1 = ax.bar(x_pos - bar_width/2, all_fcf, bar_width,
                      label='Future Value', color='#3498db', alpha=0.8)
        bars2 = ax.bar(x_pos + bar_width/2, all_pv, bar_width,
                      label='Present Value', color='#e74c3c', alpha=0.8)

        # Customize chart
        ax.set_xlabel('Year', color='white', fontsize=12)
        ax.set_ylabel('Cash Flow (Millions USD)', color='white', fontsize=12)
        ax.set_title('DCF Cash Flow Projections', color='white', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_years)
        ax.legend(facecolor='#2b2b2b', edgecolor='white')

        # Professional value annotations
        for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            height1 = bar1.get_height()
            height2 = bar2.get_height()

            ax.text(bar1.get_x() + bar1.get_width()/2., height1 + max(all_fcf) * 0.01,
                   f'${height1:.0f}M', ha='center', va='bottom', color='white', fontsize=9)
            ax.text(bar2.get_x() + bar2.get_width()/2., height2 + max(all_fcf) * 0.01,
                   f'${height2:.0f}M', ha='center', va='bottom', color='white', fontsize=9)

        # Style the axes
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')

        fig.tight_layout()

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas

    def create_sensitivity_chart(self, parent, sensitivity_results):
        """
        Generate professional sensitivity analysis tornado chart.

        Creates horizontal tornado chart showing impact ranges of key variables
        on intrinsic valuation with color-coded upside/downside impacts.

        Args:
            parent: Tkinter parent container widget
            sensitivity_results: Dictionary containing sensitivity analysis data

        Returns:
            FigureCanvasTkAgg: Embedded chart canvas for GUI integration
        """
        fig = Figure(figsize=(10, 6), facecolor='#1c1c1c')
        ax = fig.add_subplot(111, facecolor='#2b2b2b')

        variable_names = {
            'growth_rate': 'FCF Growth Rate',
            'wacc': 'WACC',
            'terminal_growth_rate': 'Terminal Growth'
        }

        # Prepare data for tornado chart
        variables = []
        low_values = []
        high_values = []
        ranges = []

        for variable, results in sensitivity_results.items():
            if variable in variable_names:
                variables.append(variable_names[variable])

                # Get the range of percentage changes
                changes = [r['percentage_change'] for r in results]
                low_values.append(min(changes))
                high_values.append(max(changes))
                ranges.append(max(changes) - min(changes))

        # Sort by range (largest impact first)
        sorted_data = sorted(zip(variables, low_values, high_values, ranges),
                           key=lambda x: x[3], reverse=True)
        variables, low_values, high_values, ranges = zip(*sorted_data)

        # Create horizontal bar chart
        y_pos = np.arange(len(variables))

        # Create bars from 0 to low_values and from 0 to high_values
        bars_low = ax.barh(y_pos, low_values, height=0.6,
                          color='#e74c3c', alpha=0.8, label='Downside Impact')
        bars_high = ax.barh(y_pos, high_values, height=0.6,
                           color='#2ecc71', alpha=0.8, label='Upside Impact')

        # Customize chart
        ax.set_xlabel('Impact on Intrinsic Value (%)', color='white', fontsize=12)
        ax.set_title('Sensitivity Analysis - Variable Impact Assessment', color='white', fontsize=14, fontweight='bold')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.legend(facecolor='#2b2b2b', edgecolor='white')

        # Add value labels
        for i, (low, high) in enumerate(zip(low_values, high_values)):
            ax.text(low - abs(low) * 0.05, i, f'{low:.1f}%',
                   ha='right', va='center', color='white', fontsize=10)
            ax.text(high + abs(high) * 0.05, i, f'{high:.1f}%',
                   ha='left', va='center', color='white', fontsize=10)

        # Add vertical line at zero
        ax.axvline(x=0, color='white', linestyle='-', alpha=0.5)

        # Style the axes
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')

        fig.tight_layout()

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas

    def create_scenario_chart(self, parent, scenario_results):
        """
        Generate professional scenario analysis comparison chart.

        Creates comparative visualization of Bear/Base/Bull case valuations
        with color-coded scenarios and detailed value annotations.

        Args:
            parent: Tkinter parent container widget
            scenario_results: Dictionary containing scenario analysis results

        Returns:
            FigureCanvasTkAgg: Embedded chart canvas for GUI integration
        """
        fig = Figure(figsize=(8, 6), facecolor='#1c1c1c')
        ax = fig.add_subplot(111, facecolor='#2b2b2b')

        scenarios = []
        intrinsic_values = []
        upside_percentages = []
        colors = []

        color_map = {
            'Bear Case': '#e74c3c',
            'Base Case': '#f39c12',
            'Bull Case': '#2ecc71'
        }

        for scenario, results in scenario_results.items():
            if 'error' not in results:
                scenarios.append(scenario)
                intrinsic_values.append(results['intrinsic_value'])
                upside_percentages.append(results['upside_percentage'])
                colors.append(color_map.get(scenario, '#3498db'))

        # Create dual-axis chart
        x_pos = np.arange(len(scenarios))

        # Primary axis - Intrinsic Values
        bars1 = ax.bar(x_pos, intrinsic_values, color=colors, alpha=0.8, width=0.6)
        ax.set_xlabel('Scenario', color='white', fontsize=12)
        ax.set_ylabel('Intrinsic Value (USD)', color='white', fontsize=12)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenarios)

        # Add value labels on bars
        for bar, value, upside in zip(bars1, intrinsic_values, upside_percentages):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(intrinsic_values) * 0.02,
                   f'${value:.2f}\n({upside:+.1f}%)', ha='center', va='bottom',
                   color='white', fontsize=10, fontweight='bold')

        # Customize chart
        ax.set_title('Scenario Analysis - Valuation Range Assessment',
                    color='white', fontsize=14, fontweight='bold')

        # Style the axes
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')

        fig.tight_layout()

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas

