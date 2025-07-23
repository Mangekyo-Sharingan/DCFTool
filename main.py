# main.py

import sv_ttk
from gui.app_window import DCFAnalyzerApp

def main():
    # Create the main window instance.
    # The app itself will handle setting the theme.
    app = DCFAnalyzerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
