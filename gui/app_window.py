# gui/app_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import sv_ttk
import threading

from models.dcf_model import DiscountedCashFlowModel
from data.data_processor import DataProcessor


class DCFAnalyzerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("DCF Valuation Tool")
        self.geometry("1100x750")

        # Set the theme
        sv_ttk.set_theme("dark")

        self.data_processor = DataProcessor()
        self.industry = 'N/A'  # Initialize industry
        self._create_panes()
        self._create_controls()
        self._create_results_display()

    def _create_panes(self):
        self.main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.controls_pane = ttk.Frame(self.main_pane, width=400)
        self.results_pane = ttk.Frame(self.main_pane)

        self.main_pane.add(self.controls_pane, weight=1)
        self.main_pane.add(self.results_pane, weight=2)

        # Prevent the control pane from being resized too small
        self.controls_pane.pack_propagate(False)

    def _create_controls(self):
        # --- Data Input Frame ---
        input_frame = ttk.LabelFrame(self.controls_pane, text="Data Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(input_frame, text="Yahoo Finance Ticker:").pack(anchor='w')
        ticker_frame = ttk.Frame(input_frame)
        ticker_frame.pack(fill=tk.X, pady=(2, 5))
        self.ticker_var = tk.StringVar(value="AAPL")
        ttk.Entry(ticker_frame, textvariable=self.ticker_var, width=10).pack(side=tk.LEFT, padx=(0, 5))
        self.fetch_button = ttk.Button(ticker_frame, text="Fetch Data", command=self._fetch_data_threaded)
        self.fetch_button.pack(side=tk.LEFT)

        # --- DCF Parameters Frame ---
        params_frame = ttk.LabelFrame(self.controls_pane, text="DCF Parameters", padding=10)
        params_frame.pack(fill=tk.X, padx=10, pady=10)

        self.dcf_params = {}
        param_config = {
            'enterprise_value': ('Enterprise Value (M)', 0.0), 'debt': ('Total Debt (M)', 0.0),
            'cash': ('Cash & Equivalents (M)', 0.0), 'shares_outstanding': ('Shares Outstanding (M)', 0.0),
            'last_fcf': ('Last FCF (M)', 0.0), 'growth_rate': ('FCF Growth Rate (%)', 5.0),
            'wacc': ('WACC (%)', 8.0), 'terminal_growth_rate': ('Terminal Growth Rate (%)', 2.0)
        }

        for i, (param, (display_name, default_val)) in enumerate(param_config.items()):
            ttk.Label(params_frame, text=f"{display_name}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
            self.dcf_params[param] = tk.DoubleVar(value=default_val)
            entry = ttk.Entry(params_frame, textvariable=self.dcf_params[param], width=15)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=3)
        params_frame.columnconfigure(1, weight=1)

        # --- Analysis Frame ---
        analysis_frame = ttk.LabelFrame(self.controls_pane, text="Analysis", padding=10)
        analysis_frame.pack(fill=tk.X, padx=10, pady=10)

        self.projection_years_var = tk.IntVar(value=5)
        ttk.Label(analysis_frame, text="Projection Years:").pack(anchor='w')
        ttk.Scale(analysis_frame, from_=3, to=10, variable=self.projection_years_var, orient=tk.HORIZONTAL,
                  command=lambda s: self.projection_years_var.set(int(float(s)))).pack(fill=tk.X, pady=(0, 5))
        self.year_label = ttk.Label(analysis_frame, textvariable=self.projection_years_var)
        self.year_label.pack(anchor='center', pady=(0, 10))

        self.calculate_button = ttk.Button(analysis_frame, text="Calculate DCF", command=self.calculate_dcf,
                                           style="Accent.TButton")
        self.calculate_button.pack(fill=tk.X, pady=5, ipady=5)

    def _create_results_display(self):
        # --- Summary Results Frame ---
        results_frame = ttk.LabelFrame(self.results_pane, text="DCF Results Summary", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        self.results_text = tk.Text(results_frame, height=15, font=('Courier', 10), wrap='word', relief='flat')
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.insert(tk.END, "Enter a ticker and click 'Fetch Data' to begin.")

        # --- Cash Flow Table Frame ---
        table_frame = ttk.LabelFrame(self.results_pane, text="Cash Flow Projections", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 10))

        self.cf_table = ttk.Treeview(table_frame, columns=("year", "fcf", "pv_fcf"), show='headings', height=8)
        self.cf_table.heading("year", text="Year")
        self.cf_table.heading("fcf", text="Projected FCF (M)")
        self.cf_table.heading("pv_fcf", text="Present Value (M)")
        self.cf_table.column("year", width=80, anchor='center')
        self.cf_table.column("fcf", width=150, anchor='e')
        self.cf_table.column("pv_fcf", width=150, anchor='e')
        self.cf_table.pack(fill=tk.BOTH, expand=True)

    def _fetch_data_threaded(self):
        """Initiates data fetching in a new thread to keep the UI responsive."""
        ticker = self.ticker_var.get().strip().upper()
        if not ticker:
            messagebox.showerror("Error", "Please enter a ticker symbol.")
            return

        self.fetch_button.config(state="disabled", text="Fetching...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Fetching data for {ticker}...")

        thread = threading.Thread(target=self._fetch_data_worker, args=(ticker,))
        thread.start()

    def _fetch_data_worker(self, ticker):
        """The actual data fetching logic that runs in a separate thread."""
        try:
            params = self.data_processor.fetch_yahoo_data(ticker)
            self.after(0, self._update_params_from_fetch, params)
        except Exception as e:
            self.after(0, messagebox.showerror, "Error", f"Failed to fetch data for {ticker}:\n{e}")
        finally:
            self.after(0, self._reset_fetch_button)

    def _update_params_from_fetch(self, params):
        """Updates the GUI with the fetched data."""
        # Set DoubleVar with the number directly, not a formatted string.
        self.dcf_params['enterprise_value'].set(params['enterprise_value'])
        self.dcf_params['debt'].set(params['debt'])
        self.dcf_params['cash'].set(params['cash'])
        self.dcf_params['shares_outstanding'].set(params['shares_outstanding'])
        self.dcf_params['last_fcf'].set(params['last_fcf'])
        self.dcf_params['growth_rate'].set(params['growth_rate'] * 100)  # Convert to percentage

        self.results_text.delete(1.0, tk.END)

        # Add debug information to help identify data issues
        debug_info = (f"Data for {self.ticker_var.get()} loaded successfully.\n"
                      f"Industry: {params['industry']}\n"
                      f"Enterprise Value: ${params['enterprise_value']:.2f}M\n"
                      f"Last FCF: ${params['last_fcf']:.2f}M\n"
                      f"Growth Rate: {params['growth_rate']:.2%}\n"
                      f"Debt: ${params['debt']:.2f}M\n"
                      f"Cash: ${params['cash']:.2f}M\n"
                      f"Shares Outstanding: {params['shares_outstanding']:.2f}M\n"
                      "Adjust parameters if needed and click 'Calculate DCF'.")

        self.results_text.insert(tk.END, debug_info)
        # Store industry for later use
        self.industry = params['industry']

    def _reset_fetch_button(self):
        """Resets the fetch button to its normal state."""
        self.fetch_button.config(state="normal", text="Fetch Data")

    def calculate_dcf(self):
        """Gathers parameters, runs the DCF model, and displays the results."""
        try:
            # Gather and convert parameters
            params_values = {name: var.get() for name, var in self.dcf_params.items()}
            # Convert percentages back to decimals
            params_values['growth_rate'] /= 100
            params_values['wacc'] /= 100
            params_values['terminal_growth_rate'] /= 100
            params_values['industry'] = self.industry

            years = self.projection_years_var.get()

            # Run model
            model = DiscountedCashFlowModel(**params_values)
            intrinsic_value = model.calculate_intrinsic_value(years)
            current_price = model.calculate_implied_share_price()

            # Get values for display
            projected_fcf = model.project_free_cash_flows(years)
            terminal_value = model.calculate_terminal_value(projected_fcf[-1])
            intrinsic_ev = model.calculate_present_value(projected_fcf, terminal_value)

            self._display_dcf_results(model, intrinsic_value, current_price, intrinsic_ev, terminal_value, years)
            self._update_cf_table(projected_fcf, model.wacc, terminal_value, years)

        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred during calculation:\n{e}")

    def _display_dcf_results(self, model, intrinsic_value, current_price, enterprise_value, terminal_value, years):
        """Formats and displays the final valuation results in the text widget."""
        self.results_text.delete(1.0, tk.END)
        upside = ((intrinsic_value - current_price) / current_price * 100) if current_price else 0
        summary = "UNDERVALUED" if intrinsic_value > current_price else "OVERVALUED"

        results_string = f"""
=== DCF VALUATION: {self.ticker_var.get()} ===

SHARE PRICE ANALYSIS:
Intrinsic Value per Share: ${intrinsic_value:10.2f}
Current Implied Price:     ${current_price:10.2f}
Upside/Downside:           {upside:10.1f}%
Summary:                   {summary} by ${abs(intrinsic_value - current_price):.2f}

CALCULATED VALUES (in Millions):
Intrinsic Enterprise Value: ${enterprise_value:10,.0f}
Terminal Value (PV):       ${terminal_value / ((1 + model.wacc) ** years):10,.0f}
Intrinsic Equity Value:    ${enterprise_value - model.debt + model.cash:10,.0f}

KEY ASSUMPTIONS:
FCF Growth Rate:           {model.growth_rate:.2%}
WACC:                      {model.wacc:.2%}
Terminal Growth Rate:      {model.terminal_growth_rate:.2%}
Projection Years:          {years}
"""
        self.results_text.insert(tk.END, results_string)

    def _update_cf_table(self, projected_fcf, wacc, terminal_value, years):
        """Populates the Treeview with cash flow projection data."""
        for item in self.cf_table.get_children():
            self.cf_table.delete(item)

        for i, fcf in enumerate(projected_fcf):
            year = i + 1
            pv_fcf = fcf / ((1 + wacc) ** year)
            # Display values with proper formatting - values are already in millions
            self.cf_table.insert("", "end", values=(f"Year {year}", f"${fcf:,.1f}M", f"${pv_fcf:,.1f}M"))

        pv_terminal = terminal_value / ((1 + wacc) ** years)
        # Display terminal value with proper formatting
        self.cf_table.insert("", "end", values=("Terminal", f"${terminal_value:,.1f}M", f"${pv_terminal:,.1f}M"))