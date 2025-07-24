"""
Financial Data Processor - Yahoo Finance Integration

This module handles fetching and processing financial data from Yahoo Finance
for use in DCF calculations.
"""

import pandas as pd
import yfinance as yf

class DataProcessor:
    """
    Handles fetching and processing financial data from Yahoo Finance.

    This class provides methods to retrieve key financial metrics needed
    for DCF analysis including cash flows, balance sheet items, and growth rates.
    """

    def fetch_yahoo_data(self, ticker):
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or info.get('trailingPE') is None:  # trailingPE is a good proxy for a valid stock
            raise ValueError(f"Invalid ticker or no data found for {ticker}")

        # Fetch financial statements
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow

        # Extract parameters (values are in millions for easier display)
        ev = info.get('enterpriseValue', 0) / 1_000_000
        debt = info.get('totalDebt', balance_sheet.loc['Total Debt'].iloc[
            0] if 'Total Debt' in balance_sheet.index else 0) / 1_000_000
        cash = info.get('totalCash', 0) / 1_000_000
        shares = info.get('sharesOutstanding', 0) / 1_000_000
########################################################################################################################
        # Calculate latest Free Cash Flow (FCF = Operating Cash Flow - Capex)
        try:
            # Try multiple possible row names for operating cash flow
            op_cash_flow = 0
            for op_name in ['Total Cash From Operating Activities', 'Operating Cash Flow', 'Cash From Operations']:
                if op_name in cash_flow.index:
                    op_cash_flow = cash_flow.loc[op_name].iloc[0]
                    break
            capex = 0
            for capex_name in ['Capital Expenditures', 'Capital Expenditure', 'Capex']:
                if capex_name in cash_flow.index:
                    capex = cash_flow.loc[capex_name].iloc[0]
                    break
            op_cash_flow = op_cash_flow if pd.notna(op_cash_flow) else 0
            capex = capex if pd.notna(capex) else 0
            last_fcf = (op_cash_flow + capex) / 1_000_000  # Capex is usually negative
            # If FCF is 0 or negative, try to get it from free cash flow directly
            if last_fcf <= 0:
                for fcf_name in ['Free Cash Flow', 'FreeCashFlow']:
                    if fcf_name in cash_flow.index:
                        direct_fcf = cash_flow.loc[fcf_name].iloc[0]
                        if pd.notna(direct_fcf) and direct_fcf > 0:
                            last_fcf = direct_fcf / 1_000_000
                            break

            # Final fallback: use a reasonable estimate based on net income
            if last_fcf <= 0:
                try:
                    net_income = financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else 0
                    if net_income > 0:
                        last_fcf = (net_income * 0.8) / 1_000_000  # Rough estimate: 80% of net income
                except (KeyError, IndexError):
                    last_fcf = 100  # Minimum fallback value in millions

        except (KeyError, IndexError, AttributeError) as e:
            print(f"Error calculating FCF: {e}")
            last_fcf = 100  # Default fallback value in millions
########################################################################################################################
        try:
            revenues = financials.loc['Total Revenue']
            growth_rates = revenues.pct_change(periods=-1, fill_method=None).dropna()
            avg_growth = growth_rates.head(3).mean() if not growth_rates.empty else 0.05
            growth_rate = min(max(avg_growth, 0.01), 0.20)  # Constrain between 1% and 20%
        except (KeyError, IndexError):
            growth_rate = 0.05  # Default growth rate if data is unavailable

        return {
            "enterprise_value": ev,
            "debt": debt,
            "cash": cash,
            "shares_outstanding": shares,
            "last_fcf": last_fcf,
            "growth_rate": growth_rate,
            "industry": info.get('industry', 'N/A')
        }
