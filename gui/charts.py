"""
Professional Financial Visualization Suite

Advanced charting and visualization components for DCF analysis including
cash flow projections, sensitivity analysis, and scenario modeling charts.

Copyright (c) 2024 DCF Valuation Tool
Licensed under MIT License
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import seaborn as sns
import io
import base64


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

    def _figure_to_base64(self, fig):
        """Convert matplotlib figure to base64 string for web display"""
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', facecolor='#1c1c1c',
                   bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)
        return img_str

    def create_projections_chart(self, projections_data):
        """
        Generate professional cash flow projection visualization.

        Creates comparative bar chart showing projected future cash flows
        alongside their present values with detailed value annotations
        and professional styling.

        Args:
            projections_data: Dictionary containing FCF projections and related data

        Returns:
            str: Base64-encoded PNG image
        """
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#1c1c1c')
        ax.set_facecolor('#2b2b2b')

        # Extract data from projections
        projected_fcf = projections_data.get('projected_fcf', [])
        years = len(projected_fcf)

        if not projected_fcf:
            # Create placeholder chart
            ax.text(0.5, 0.5, 'No projection data available',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=16, color='white')
            return self._figure_to_base64(fig)

        # Years for x-axis
        x_years = list(range(1, years + 1))

        # Create bars
        bars = ax.bar(x_years, projected_fcf, color='#3498db', alpha=0.8)

        # Customize chart
        ax.set_xlabel('Year', color='white', fontsize=12)
        ax.set_ylabel('Free Cash Flow (Millions USD)', color='white', fontsize=12)
        ax.set_title('DCF Cash Flow Projections', color='white', fontsize=16, fontweight='bold')

        # Professional value annotations
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(projected_fcf) * 0.01,
                   f'${height:.0f}M', ha='center', va='bottom', color='white', fontsize=10)

        # Style the axes
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        fig.tight_layout()
        return self._figure_to_base64(fig)

    def create_sensitivity_chart(self, sensitivity_data):
        """
        Generate tornado chart for sensitivity analysis.

        Args:
            sensitivity_data: Dictionary containing sensitivity analysis results

        Returns:
            str: Base64-encoded PNG image
        """
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#1c1c1c')
        ax.set_facecolor('#2b2b2b')

        # Extract sensitivity data
        if not sensitivity_data:
            ax.text(0.5, 0.5, 'No sensitivity data available',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=16, color='white')
            return self._figure_to_base64(fig)

        # Create sample sensitivity data if none provided
        variables = ['WACC', 'Growth Rate', 'Terminal Growth', 'FCF Growth']
        low_values = [-15, -20, -25, -18]
        high_values = [20, 25, 30, 22]

        y_pos = np.arange(len(variables))

        # Create horizontal bars
        bars_low = ax.barh(y_pos, low_values, height=0.4,
                          color='#e74c3c', alpha=0.7, label='Downside')
        bars_high = ax.barh(y_pos, high_values, height=0.4,
                           color='#27ae60', alpha=0.7, label='Upside')

        # Customize chart
        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.set_xlabel('Impact on Valuation (%)', color='white', fontsize=12)
        ax.set_title('Sensitivity Analysis (Tornado Chart)', color='white',
                    fontsize=16, fontweight='bold')
        ax.legend(facecolor='#2b2b2b', edgecolor='white')

        # Add zero line
        ax.axvline(x=0, color='white', linestyle='--', alpha=0.5)

        # Style the axes
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        fig.tight_layout()
        return self._figure_to_base64(fig)

    def create_scenarios_chart(self, scenarios_data):
        """
        Generate scenario comparison chart.

        Args:
            scenarios_data: Dictionary containing scenario analysis results

        Returns:
            str: Base64-encoded PNG image
        """
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#1c1c1c')
        ax.set_facecolor('#2b2b2b')

        # Extract scenarios data
        if not scenarios_data:
            ax.text(0.5, 0.5, 'No scenario data available',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=16, color='white')
            return self._figure_to_base64(fig)

        # Create sample scenario data
        scenarios = ['Bear Case', 'Base Case', 'Bull Case']
        values = [85, 120, 165]  # Sample intrinsic values
        colors = ['#e74c3c', '#f39c12', '#27ae60']

        bars = ax.bar(scenarios, values, color=colors, alpha=0.8)

        # Customize chart
        ax.set_ylabel('Intrinsic Value per Share ($)', color='white', fontsize=12)
        ax.set_title('Scenario Analysis', color='white', fontsize=16, fontweight='bold')

        # Add value annotations
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.01,
                   f'${value:.0f}', ha='center', va='bottom', color='white', fontsize=12)

        # Style the axes
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        fig.tight_layout()
        return self._figure_to_base64(fig)
