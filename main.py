"""
DCF Valuation Tool - Main Entry Point
A professional-grade Discounted Cash Flow analysis application
"""

import sys
from gui.app_window import DCFAnalyzerApp

def main():
    """Main application entry point"""
    try:
        # Create and run the main application window
        app = DCFAnalyzerApp()
        app.mainloop()
    except ImportError as e:
        print(f"Error: Missing required dependencies. Please install requirements: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
