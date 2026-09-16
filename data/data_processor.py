"""
Fetches and normalises financial data from Yahoo Finance for DCF analysis.
"""

import pandas as pd
import yfinance as yf


class DataProcessor:
    """Pulls key financials from yfinance and returns a dict ready for
    the DCF model (all monetary values in millions)."""

    def fetch_yahoo_data(self, ticker):
        """Fetch financial data for *ticker* from Yahoo Finance.

        Returns a dict with enterprise_value, debt, cash,
        shares_outstanding, last_fcf, growth_rate, industry,
        and current_price -- all monetary values normalised to millions.

        Raises ValueError if the ticker is invalid or has no data.
        """
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info:
            raise ValueError(f"Invalid ticker or no data for '{ticker}'")

        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow

        # Core metrics (normalised to millions)
        ev = info.get("enterpriseValue", 0) / 1_000_000
        debt = (
            info.get(
                "totalDebt",
                balance_sheet.loc["Total Debt"].iloc[0]
                if "Total Debt" in balance_sheet.index
                else 0,
            )
            / 1_000_000
        )
        cash = info.get("totalCash", 0) / 1_000_000
        shares = info.get("sharesOutstanding", 0) / 1_000_000

        current_price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose", 0)
        )

        # --- Free cash flow (with fallbacks) ---
        last_fcf = self._extract_fcf(cash_flow, financials)

        # --- Historical growth rate from revenue ---
        growth_rate = self._calc_growth_rate(financials)

        return {
            "enterprise_value": ev,
            "debt": debt,
            "cash": cash,
            "shares_outstanding": shares,
            "last_fcf": last_fcf,
            "growth_rate": growth_rate,
            "industry": info.get("industry", "N/A"),
            "current_price": current_price,
        }

    # ------------------------------------------------------------------

    @staticmethod
    def _extract_fcf(cash_flow, financials):
        """Try multiple approaches to get FCF from the statements."""
        try:
            # 1) operating cash flow + capex
            op = 0
            for name in [
                "Total Cash From Operating Activities",
                "Operating Cash Flow",
                "Cash From Operations",
            ]:
                if name in cash_flow.index:
                    op = cash_flow.loc[name].iloc[0]
                    break

            capex = 0
            for name in ["Capital Expenditures", "Capital Expenditure", "Capex"]:
                if name in cash_flow.index:
                    capex = cash_flow.loc[name].iloc[0]
                    break

            op = op if pd.notna(op) else 0
            capex = capex if pd.notna(capex) else 0
            fcf = (op + capex) / 1_000_000

            # 2) direct FCF field
            if fcf <= 0:
                for name in ["Free Cash Flow", "FreeCashFlow"]:
                    if name in cash_flow.index:
                        val = cash_flow.loc[name].iloc[0]
                        if pd.notna(val) and val > 0:
                            fcf = val / 1_000_000
                            break

            # 3) rough estimate from net income
            if fcf <= 0:
                try:
                    ni = (
                        financials.loc["Net Income"].iloc[0]
                        if "Net Income" in financials.index
                        else 0
                    )
                    if ni > 0:
                        fcf = (ni * 0.8) / 1_000_000
                except (KeyError, IndexError):
                    fcf = 100  # last-resort fallback

        except (KeyError, IndexError, AttributeError) as exc:
            print(f"FCF warning: {exc}")
            fcf = 100

        return fcf

    @staticmethod
    def _calc_growth_rate(financials):
        """Compute average revenue growth, clamped to -20% to 50%."""
        try:
            revenues = financials.loc["Total Revenue"]
            changes = revenues.pct_change(periods=-1, fill_method=None).dropna()
            avg = changes.head(3).mean() if not changes.empty else 0.05
            return min(max(avg, -0.20), 0.50)
        except (KeyError, IndexError):
            return 0.05
