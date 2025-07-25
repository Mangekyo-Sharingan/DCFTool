# DCF Valuation Tool

A professional-grade Discounted Cash Flow (DCF) valuation application for analyzing publicly traded companies. The application fetches real-time financial data and provides comprehensive valuation analysis with advanced sensitivity and scenario modeling capabilities.

## Key Features

- **Professional GUI Interface:** Modern dark-themed interface built with tkinter and enhanced styling
- **Real-time Data Integration:** Automated financial data retrieval from Yahoo Finance API
- **Comprehensive DCF Analysis:** Full DCF modeling with customizable parameters and multi-year projections
- **Advanced Analytics:** Built-in sensitivity analysis and scenario modeling (Bear/Base/Bull cases)
- **Visual Data Representation:** Professional charts for cash flow projections and sensitivity analysis
- **Robust Error Handling:** Comprehensive validation and error management for reliable operation
- **Multi-threaded Architecture:** Non-blocking data retrieval maintains responsive user interface

## Advanced Analysis Capabilities

### Sensitivity Analysis
- **Multi-variable Impact Assessment:** Analyzes how changes in growth rates, WACC, and terminal growth affect valuation
- **Tornado Chart Visualization:** Professional visualization showing variable impact ranges
- **Risk Assessment Tools:** Quantifies valuation uncertainty and identifies key value drivers

### Scenario Modeling
- **Three-Case Analysis:** Conservative (Bear), Base, and Optimistic (Bull) scenarios
- **Parameter Optimization:** Automatic adjustment of growth rates and discount rates for each scenario
- **Comparative Analysis:** Side-by-side valuation comparison with upside/downside calculations

### Professional Visualizations
- **Cash Flow Projection Charts:** Comparative visualization of future vs. present value cash flows
- **Sensitivity Tornado Charts:** Horizontal bar charts displaying variable impact ranges
- **Scenario Comparison Charts:** Professional styling with clear value annotations and percentage changes

## Technical Architecture
```
DCFtool/
├── main.py                    # Application entry point and initialization
├── requirements.txt           # Production dependencies specification
├── setup.py                   # Package distribution configuration
├── gui/
│   ├── __init__.py           # GUI package initialization
│   ├── app_window.py         # Main application interface and user controls
│   └── charts.py             # Data visualization and charting components
├── data/
│   ├── __init__.py           # Data package initialization
│   └── data_processor.py     # Financial data acquisition and processing
├── models/
│   ├── __init__.py           # Models package initialization
│   └── dcf_model.py          # Core DCF calculation engine
└── tests/
    ├── __init__.py           # Test package initialization
    ├── test_data_processor.py # Data processing unit tests
    └── test_dcf_model.py      # DCF model calculation tests
```

## System Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python:** 3.7 or higher
- **Internet Connection:** Required for fetching financial data

## Dependencies

Core dependencies managed via requirements.txt:
- `yfinance` - Financial data API integration
- `sv-ttk` - Modern UI theming system
- `tkinterdnd2` - Enhanced drag-and-drop functionality
- `pandas` - High-performance data manipulation
- `numpy` - Numerical computing foundation
- `matplotlib` - Advanced plotting and visualization
- `seaborn` - Statistical data visualization

## Installation Guide

### Quick Start Installation

1. **Download and Extract:**
   ```bash
   git clone https://github.com/Mangekyo-Sharingan/DCFTool.git
   cd DCFtool
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Application:**
   ```bash
   python main.py
   ```

### Professional Package Installation

1. **Install as Development Package:**
   ```bash
   pip install -e .
   ```

2. **Run from Command Line:**
   ```bash
   python -m dcftool
   ```

## User Guide

### Basic Operation
1. Launch the application using `python main.py`
2. Enter a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
3. Click "Fetch Data" to populate DCF parameters automatically
4. Review and adjust parameters as needed for your analysis
5. Configure projection period using the year slider (3-10 years)
6. Execute "Calculate DCF" to generate comprehensive valuation results

### Advanced Features
- **Tabbed Results Interface:** Navigate between summary, charts, and analysis views
- **Sensitivity Analysis:** Automatic generation of tornado charts showing variable impacts
- **Scenario Comparison:** Bear/Base/Bull case analysis with comparative visualizations
- **Data Export:** Professional charts suitable for presentations and reports

## Quality Assurance

### Automated Testing
```bash
# Execute comprehensive test suite
python -m unittest discover tests -v

# Run specific test modules
python -m unittest tests.test_dcf_model -v
python -m unittest tests.test_data_processor -v

# Generate coverage reports
pip install coverage
coverage run -m unittest discover tests
coverage report -m
coverage html
```

## Distribution and Deployment

### Standalone Executable Creation
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Cross-Platform Package Building
```bash
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
```

## Core Components

- **DCFAnalyzerApp:** Primary application controller managing user interface and workflow
- **DataProcessor:** Financial data acquisition system with robust error handling
- **DiscountedCashFlowModel:** Enterprise-grade DCF calculation engine with advanced analytics
- **DCFCharts:** Professional visualization system for data presentation
- **Comprehensive Test Suite:** Production-quality unit tests ensuring reliability

## Troubleshooting

- **Network Issues:** Verify internet connectivity for Yahoo Finance API access
- **Invalid Ticker Symbols:** Confirm ticker exists and is publicly traded
- **Theme Loading:** Ensure sv-ttk package is correctly installed
- **Permission Errors:** Run installation with appropriate system permissions
- **Memory Issues:** Close other applications if experiencing performance degradation

## Support and Maintenance

This application is designed for professional financial analysis and maintains compatibility with current Python ecosystems. Regular updates ensure continued compatibility with financial data sources and operating system requirements.

## License
