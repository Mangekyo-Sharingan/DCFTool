"""
Matplotlib chart generators for the DCF web app.
Returns base64-encoded PNGs that get embedded in the page.
"""

import io
import base64
import numpy as np
import matplotlib

matplotlib.use("Agg")  # non-interactive backend (no GUI needed)
import matplotlib.pyplot as plt
import seaborn as sns


class DCFCharts:
    def __init__(self):
        plt.style.use("dark_background")
        sns.set_palette("husl")

    @staticmethod
    def _to_base64(fig):
        buf = io.BytesIO()
        fig.savefig(
            buf, format="png", facecolor="#1c1c1c", bbox_inches="tight", dpi=100
        )
        buf.seek(0)
        encoded = base64.b64encode(buf.getvalue()).decode()
        plt.close(fig)
        return encoded

    # ----- projections chart -----

    def create_projections_chart(self, data):
        """Bar chart of projected free cash flows."""
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="#1c1c1c")
        ax.set_facecolor("#2b2b2b")

        fcfs = data.get("projected_fcf", [])
        if not fcfs:
            ax.text(
                0.5,
                0.5,
                "No projection data",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=16,
                color="white",
            )
            return self._to_base64(fig)

        years = list(range(1, len(fcfs) + 1))
        bars = ax.bar(years, fcfs, color="#3498db", alpha=0.8)

        ax.set_xlabel("Year", color="white", fontsize=12)
        ax.set_ylabel("Free Cash Flow ($M)", color="white", fontsize=12)
        ax.set_title(
            "Projected Free Cash Flows", color="white", fontsize=16, fontweight="bold"
        )

        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + max(fcfs) * 0.01,
                f"${h:.0f}M",
                ha="center",
                va="bottom",
                color="white",
                fontsize=10,
            )

        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")

        fig.tight_layout()
        return self._to_base64(fig)

    # ----- sensitivity tornado chart -----

    def create_sensitivity_chart(self, sensitivity_data):
        """Horizontal tornado chart showing how each variable moves the
        intrinsic value relative to the base case."""
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="#1c1c1c")
        ax.set_facecolor("#2b2b2b")

        if not sensitivity_data:
            ax.text(
                0.5,
                0.5,
                "No sensitivity data",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=16,
                color="white",
            )
            return self._to_base64(fig)

        # Build tornado bars from actual sensitivity results
        labels = {
            "growth_rate": "Growth Rate",
            "wacc": "WACC",
            "terminal_growth_rate": "Terminal Growth",
        }
        variables = []
        low_vals = []
        high_vals = []

        for var, results in sensitivity_data.items():
            pct_changes = [r["percentage_change"] for r in results]
            lo = min(pct_changes)
            hi = max(pct_changes)
            variables.append(labels.get(var, var))
            low_vals.append(lo)
            high_vals.append(hi)

        y_pos = np.arange(len(variables))
        ax.barh(
            y_pos, low_vals, height=0.4, color="#e74c3c", alpha=0.7, label="Downside"
        )
        ax.barh(
            y_pos, high_vals, height=0.4, color="#27ae60", alpha=0.7, label="Upside"
        )

        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.set_xlabel("Impact on Valuation (%)", color="white", fontsize=12)
        ax.set_title(
            "Sensitivity Analysis", color="white", fontsize=16, fontweight="bold"
        )
        ax.legend(facecolor="#2b2b2b", edgecolor="white")
        ax.axvline(x=0, color="white", linestyle="--", alpha=0.5)

        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")

        fig.tight_layout()
        return self._to_base64(fig)

    # ----- scenario comparison chart -----

    def create_scenarios_chart(self, scenarios_data):
        """Bar chart comparing bear / base / bull intrinsic values."""
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="#1c1c1c")
        ax.set_facecolor("#2b2b2b")

        if not scenarios_data:
            ax.text(
                0.5,
                0.5,
                "No scenario data",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=16,
                color="white",
            )
            return self._to_base64(fig)

        # Pull actual values from the scenario results
        order = ["Bear Case", "Base Case", "Bull Case"]
        colors = ["#e74c3c", "#f39c12", "#27ae60"]
        names = []
        values = []
        bar_colors = []

        for i, name in enumerate(order):
            if name in scenarios_data and "error" not in scenarios_data[name]:
                names.append(name)
                values.append(scenarios_data[name]["intrinsic_value"])
                bar_colors.append(colors[i])

        if not values:
            ax.text(
                0.5,
                0.5,
                "All scenarios failed",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=16,
                color="white",
            )
            return self._to_base64(fig)

        bars = ax.bar(names, values, color=bar_colors, alpha=0.8)

        ax.set_ylabel("Intrinsic Value / Share ($)", color="white", fontsize=12)
        ax.set_title("Scenario Analysis", color="white", fontsize=16, fontweight="bold")

        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.01,
                f"${val:.2f}",
                ha="center",
                va="bottom",
                color="white",
                fontsize=12,
            )

        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")

        fig.tight_layout()
        return self._to_base64(fig)
