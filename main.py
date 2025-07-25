"""
DCF Valuation Tool - Professional Edition

A comprehensive financial analysis application for discounted cash flow
valuation of publicly traded companies.

Author: DCF Development Team
Version: 1.0.0
License: MIT
"""

import sys
from gui.app_window import DCFAnalyzerApp

def main():
    """
    Application entry point with enhanced error handling and logging.

    Initializes the main application window and handles startup errors
    gracefully with user-friendly error messages.
    """
    try:
        app = DCFAnalyzerApp()
        app.mainloop()
    except ImportError as e:
        print(f"Dependency Error: Missing required packages. Please run 'pip install -r requirements.txt'")
        print(f"Technical Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Application Error: Failed to initialize DCF Valuation Tool")
        print(f"Technical Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
