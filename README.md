# DCF Valuation Tool

A Flask web app that calculates the intrinsic value of a stock using
[Discounted Cash Flow](https://en.wikipedia.org/wiki/Discounted_cash_flow)
analysis. Enter a ticker, pull live financials from Yahoo Finance, and get a
valuation with sensitivity and scenario breakdowns.

## How it works

1. Fetches financials (enterprise value, debt, cash, FCF, revenue growth) via
   `yfinance`.
2. Projects future free cash flows using a configurable growth rate.
3. Computes terminal value with the Gordon Growth Model.
4. Discounts everything back at the WACC to get intrinsic value per share.
5. Runs sensitivity analysis (varying growth, WACC, terminal growth) and
   bear/base/bull scenario analysis.
6. Renders charts as base64 PNGs using matplotlib.

## Quickstart

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 in your browser.

## Running tests

```bash
python -m pytest tests/
```

## Stack

- **Backend:** Flask, yfinance, pandas, numpy
- **Charts:** matplotlib, seaborn
- **Frontend:** Bootstrap 5, vanilla JS

## License

MIT
