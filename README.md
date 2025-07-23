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
├── setup.py                   # Package setup for distribution
├── gui/
│   ├── __init__.py           # Package initialization
│   └── app_window.py         # Main application window with integrated controls and results
├── data/
│   ├── __init__.py           # Package initialization
│   └── data_processor.py     # Handles data fetching and processing from Yahoo Finance
├── models/
│   ├── __init__.py           # Package initialization
│   └── dcf_model.py          # Core DCF calculation logic and valuation model
└── tests/
    ├── __init__.py           # Package initialization
    ├── test_data_processor.py # Unit tests for data processing functionality
    └── test_dcf_model.py      # Unit tests for DCF model calculations
```

## System Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python:** 3.7 or higher
- **Internet Connection:** Required for fetching financial data

## Required Dependencies

The following packages will be automatically installed (see `requirements.txt`):
- `yfinance` - Yahoo Finance data fetching
- `sv-ttk` - Modern tkinter theme
- `tkinterdnd2` - Drag and drop support
- `pandas` - Data manipulation

## Installation

### Option 1: Direct Installation

1. **Download the Project:**
   - Download and extract the project files to your desired location
   - Or clone from repository:
   ```bash
   git clone https://github.com/Mangekyo-Sharingan/DCFTool.git
   cd DCFtool
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

### Option 2: Package Installation

1. **Install as a Package:**
   ```bash
   pip install -e .
   ```

2. **Run from anywhere:**
   ```bash
   python -m dcftool
   ```

## Usage Instructions

1. **Launch the Application:**
   - Execute `python main.py` from the project directory
   - The application will open with a modern dark theme interface

2. **Perform DCF Analysis:**
   - Enter a valid stock ticker (e.g., `AAPL`, `MSFT`, `GOOGL`) into the input field
   - Click the "Fetch Data" button to automatically populate DCF parameters
   - Review and adjust the DCF parameters as needed (growth rates, WACC, etc.)
   - Set the desired projection years using the slider (3-10 years)
   - Click the "Calculate DCF" button to perform the valuation
   - View results in the summary panel and detailed cash flow projections table

## Testing

Run the included unit tests to verify functionality:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test modules
python -m unittest tests.test_dcf_model
python -m unittest tests.test_data_processor
```

## Building for Distribution

### Windows Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Cross-Platform Package
```bash
python setup.py sdist bdist_wheel
```

## Key Components

- **DCFAnalyzerApp**: Main application window with integrated controls and results display
- **DataProcessor**: Handles Yahoo Finance data fetching and financial statement processing
- **DiscountedCashFlowModel**: Core valuation model implementing DCF calculations
- **Comprehensive Testing**: Unit tests covering both data processing and model calculations

## Troubleshooting

- **Data Fetching Issues**: Ensure you have an active internet connection
- **Invalid Ticker Errors**: Verify the ticker symbol is correct and publicly traded
- **Theme Issues**: The application uses sv-ttk for theming; ensure it's properly installed
- **Permission Errors**: Run with appropriate permissions if installation fails

