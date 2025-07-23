# Python DCF Valuation Tool

This application provides a Discounted Cash Flow (DCF) valuation for a publicly traded company by fetching financial data from Yahoo Finance.

## Features

- **Simple GUI:** An easy-to-use graphical interface built with `tkinter`.
- **Dark Theme:** A modern, dark-themed UI for comfortable use.
- **Dynamic Data:** Fetches the latest financial data using the `yfinance` library.
- **Industry-Aware Modeling:** Adjusts key DCF assumptions based on the company's industry.
- **Detailed Output:** Displays the calculated intrinsic value and the assumptions used in the model.
- **OOP Design:** Built with an object-oriented structure for maintainability and scalability.

## Project Structure
dcf_tool/
├── main.py               \# Application entry point  
├── requirements.txt      \# Python dependencies  
├── gui/  
│   ├── \_\_init\_\_.py  
│   ├── main_window.py      \# Main application window  
│   ├── results_window.py   \# DCF results display window  
│   └── styles.py           \# Dark theme styling configuration  
├── data/  
│   ├── \_\_init\_\_.py  
│   └── yahoo_finance.py    \# Handles data fetching from Yahoo Finance  
└── models/  
    ├── \_\_init\_\_.py  
    └── dcf_model.py        \# Core DCF calculation logic

## How to Run

1.  **Install Dependencies:**
    Make sure you have Python 3 installed. Then, install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    Execute the `main.py` script:
    ```bash
    python main.py
    ```

3.  **Usage:**
    - Enter a valid stock ticker (e.g., `AAPL`, `MSFT`, `GOOGL`) into the input field.
    - Click the "Analyze Ticker" button.
    - The application will fetch the data and perform the calculation.
    - A new window will appear with the DCF valuation results.
