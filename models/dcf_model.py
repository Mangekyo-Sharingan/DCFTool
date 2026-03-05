"""
DCF valuation model using standard discounted cash flow methodology.
"""


class DCFModel:
    """Calculates intrinsic share value via projected free cash flows,
    terminal value (Gordon Growth), and present-value discounting."""

    def __init__(
        self,
        enterprise_value,
        debt,
        cash,
        shares_outstanding,
        last_fcf,
        growth_rate,
        wacc,
        terminal_growth_rate,
        industry="N/A",
    ):
        self.enterprise_value = enterprise_value
        self.debt = debt
        self.cash = cash
        self.shares_outstanding = shares_outstanding
        self.last_fcf = last_fcf
        self.growth_rate = growth_rate
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate
        self.industry = industry

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def project_free_cash_flows(self, years=5):
        """Return list of projected FCFs for *years* into the future."""
        return [
            self.last_fcf * (1 + self.growth_rate) ** y for y in range(1, years + 1)
        ]

    def calculate_terminal_value(self, final_fcf):
        """Gordon Growth Model: TV = FCF*(1+g) / (WACC - g)."""
        denom = self.wacc - self.terminal_growth_rate
        if denom <= 0:
            raise ValueError("WACC must be greater than terminal growth rate")
        return (final_fcf * (1 + self.terminal_growth_rate)) / denom

    def calculate_present_value(self, cash_flows, terminal_value):
        """Discount projected cash flows + terminal value back to today."""
        pv_fcf = sum(
            fcf / ((1 + self.wacc) ** (i + 1)) for i, fcf in enumerate(cash_flows)
        )
        pv_terminal = terminal_value / ((1 + self.wacc) ** len(cash_flows))
        return pv_fcf + pv_terminal

    def implied_share_price(self):
        """Current implied price from enterprise value."""
        equity = self.enterprise_value - self.debt + self.cash
        return equity / self.shares_outstanding if self.shares_outstanding else 0

    # ------------------------------------------------------------------
    # Main valuation
    # ------------------------------------------------------------------

    def intrinsic_value(self, years=5):
        """Run a full DCF and return intrinsic value per share."""
        projected = self.project_free_cash_flows(years)
        if not projected:
            return 0

        tv = self.calculate_terminal_value(projected[-1])
        ev = self.calculate_present_value(projected, tv)
        equity = ev - self.debt + self.cash

        return equity / self.shares_outstanding if self.shares_outstanding else 0

    def project_cash_flows(self, years=5):
        """Return a dict with projections, present values, and terminal value
        (used by the web API)."""
        projected = self.project_free_cash_flows(years)

        pvs = [fcf / ((1 + self.wacc) ** (i + 1)) for i, fcf in enumerate(projected)]

        final = projected[-1] if projected else 0
        try:
            tv = self.calculate_terminal_value(final) if final > 0 else 0
        except ValueError:
            tv = 0

        return {
            "projected_fcf": projected,
            "present_values": pvs,
            "terminal_value": tv,
            "years": list(range(1, years + 1)),
            "wacc": self.wacc,
            "growth_rate": self.growth_rate,
            "terminal_growth_rate": self.terminal_growth_rate,
        }

    # ------------------------------------------------------------------
    # Sensitivity & scenario analysis
    # ------------------------------------------------------------------

    def sensitivity_analysis(self, years=5, variable_ranges=None):
        """Vary key inputs and record the impact on intrinsic value.

        Returns dict mapping variable name -> list of result dicts.
        """
        if variable_ranges is None:
            variable_ranges = {
                "growth_rate": [-0.02, -0.01, 0, 0.01, 0.02],
                "wacc": [-0.01, -0.005, 0, 0.005, 0.01],
                "terminal_growth_rate": [-0.005, -0.0025, 0, 0.0025, 0.005],
            }

        base = self.intrinsic_value(years)
        results = {}

        for var, adjustments in variable_ranges.items():
            original = getattr(self, var)
            var_results = []

            for adj in adjustments:
                setattr(self, var, original + adj)
                try:
                    val = self.intrinsic_value(years)
                    pct = ((val - base) / base * 100) if base else 0
                    var_results.append(
                        {
                            "adjustment": adj,
                            "intrinsic_value": val,
                            "percentage_change": pct,
                        }
                    )
                except ValueError:
                    var_results.append(
                        {
                            "adjustment": adj,
                            "intrinsic_value": 0,
                            "percentage_change": -100,
                        }
                    )

            setattr(self, var, original)
            results[var] = var_results

        return results

    def scenario_analysis(self, years=5):
        """Bear / base / bull scenarios with hardcoded offsets."""
        scenarios = {
            "Bear Case": {
                "growth_rate_adj": -0.02,
                "wacc_adj": 0.01,
                "terminal_growth_adj": -0.005,
            },
            "Base Case": {
                "growth_rate_adj": 0,
                "wacc_adj": 0,
                "terminal_growth_adj": 0,
            },
            "Bull Case": {
                "growth_rate_adj": 0.02,
                "wacc_adj": -0.005,
                "terminal_growth_adj": 0.005,
            },
        }

        originals = {
            "growth_rate": self.growth_rate,
            "wacc": self.wacc,
            "terminal_growth_rate": self.terminal_growth_rate,
        }

        results = {}
        for name, adj in scenarios.items():
            self.growth_rate = originals["growth_rate"] + adj["growth_rate_adj"]
            self.wacc = originals["wacc"] + adj["wacc_adj"]
            self.terminal_growth_rate = (
                originals["terminal_growth_rate"] + adj["terminal_growth_adj"]
            )

            try:
                iv = self.intrinsic_value(years)
                price = self.implied_share_price()
                upside = ((iv - price) / price * 100) if price else 0
                results[name] = {
                    "intrinsic_value": iv,
                    "upside_percentage": upside,
                    "growth_rate": self.growth_rate,
                    "wacc": self.wacc,
                    "terminal_growth_rate": self.terminal_growth_rate,
                }
            except ValueError:
                results[name] = {
                    "intrinsic_value": 0,
                    "upside_percentage": -100,
                    "growth_rate": self.growth_rate,
                    "wacc": self.wacc,
                    "terminal_growth_rate": self.terminal_growth_rate,
                    "error": "Invalid parameter combination",
                }

        # restore
        for k, v in originals.items():
            setattr(self, k, v)

        return results
