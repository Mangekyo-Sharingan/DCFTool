# Python DCF Valuation Tool

This application provides a Discounted Cash Flow (DCF) valuation for publicly traded companies by fetching financial data from Yahoo Finance and allowing users to customize valuation parameters.

## Features

- **Intuitive GUI:** A user-friendly graphical interface built with `tkinter` and themed with `sv-ttk`.
- **Dark Theme:** A modern, dark-themed UI for comfortable use.
- **Automatic Data Fetching:** Retrieves the latest financial data using the `yfinance` library.
- **Customizable Parameters:** Allows manual adjustment of all DCF parameters including growth rates and WACC.
- **Real-time Calculations:** Performs DCF calculations with configurable projection periods (3-10 years).
- **Detailed Results:** Displays intrinsic value, current price comparison, and detailed cash flow projections.
- **Cash Flow Table:** Visual representation of projected free cash flows and their present values.
- **Industry Recognition:** Identifies and displays company industry information.
- **Error Handling:** Robust error handling for invalid tickers and missing data.
- **Threaded Data Fetching:** Non-blocking data retrieval to maintain UI responsiveness.

## Project Structure
```
DCFtool/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── gui/
│   └── app_window.py         # Main application window with integrated controls and results
├── data/
│   └── data_processor.py     # Handles data fetching and processing from Yahoo Finance
├── models/
│   └── dcf_model.py          # Core DCF calculation logic and valuation model
└── tests/
    ├── test_data_processor.py # Unit tests for data processing functionality
    └── test_dcf_model.py      # Unit tests for DCF model calculations
```

## Requirements

- Python 3.7+
- Required packages (see `requirements.txt`):
  - `yfinance` - Yahoo Finance data fetching
  - `sv-ttk` - Modern tkinter theme
  - `tkinterdnd2` - Drag and drop support
  - `pandas` - Data manipulation

## Installation

1. **Clone or Download the Project:**
   ```bash
   git clone <repository-url>
   cd DCFtool
   ```

2. **Install Dependencies:**
   Make sure you have Python 3.7+ installed. Then, install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. **Run the Application:**
   Execute the `main.py` script from the project directory:
   ```bash
   python main.py
   ```

2. **Usage:**
   - Enter a valid stock ticker (e.g., `AAPL`, `MSFT`, `GOOGL`) into the input field.
   - Click the "Fetch Data" button to automatically populate DCF parameters.
   - Review and adjust the DCF parameters as needed (growth rates, WACC, etc.).
   - Set the desired projection years using the slider (3-10 years).
   - Click the "Calculate DCF" button to perform the valuation.
   - View results in the summary panel and detailed cash flow projections table.

## Testing

Run the included unit tests to verify functionality:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test files
python -m unittest tests.test_dcf_model
python -m unittest tests.test_data_processor
```

## Key Components

- **DCFAnalyzerApp**: Main application window with integrated controls and results display
- **DataProcessor**: Handles Yahoo Finance data fetching and financial statement processing
- **DiscountedCashFlowModel**: Core valuation model implementing DCF calculations
- **Comprehensive Testing**: Unit tests covering both data processing and model calculations
