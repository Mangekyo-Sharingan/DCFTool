"""
DCF Analyzer Application - Main User Interface

Professional DCF valuation application with integrated data fetching,
calculation engine, and advanced analytics visualization.

Copyright (c) 2024 DCF Valuation Tool
Licensed under MIT License
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import sv_ttk
import threading

from models.dcf_model import DiscountedCashFlowModel
from data.data_processor import DataProcessor
from gui.charts import DCFCharts

class DCFAnalyzerApp(TkinterDnD.Tk):
    """
    Main application window providing comprehensive DCF analysis capabilities.

    Features integrated data fetching, parameter adjustment, DCF calculations,
    sensitivity analysis, scenario modeling, and professional visualizations.
    """

    def __init__(self):
        super().__init__()
        self.title("DCF Valuation Tool - Professional Edition")
        self.geometry("1400x900")

        sv_ttk.set_theme("dark")

        self.data_processor = DataProcessor()
        self.charts = DCFCharts()
        self.industry = 'N/A'
        self._create_panes()
        self._create_controls()
        self._create_results_display()

    def _create_panes(self):
        """Initialize main application layout with resizable panes"""
        self.main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.controls_pane = ttk.Frame(self.main_pane, width=400)
        self.results_pane = ttk.Frame(self.main_pane)

        self.main_pane.add(self.controls_pane, weight=1)
        self.main_pane.add(self.results_pane, weight=2)

        self.controls_pane.pack_propagate(False)

    def _create_controls(self):
        """Build user control interface for data input and parameter configuration"""
        # Data Input Section
        input_frame = ttk.LabelFrame(self.controls_pane, text="Data Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(input_frame, text="Yahoo Finance Ticker:").pack(anchor='w')
        ticker_frame = ttk.Frame(input_frame)
        ticker_frame.pack(fill=tk.X, pady=(2, 5))
        self.ticker_var = tk.StringVar(value="AAPL")
        ttk.Entry(ticker_frame, textvariable=self.ticker_var, width=10).pack(side=tk.LEFT, padx=(0, 5))
        self.fetch_button = ttk.Button(ticker_frame, text="Fetch Data", command=self._fetch_data_threaded)
        self.fetch_button.pack(side=tk.LEFT)

        # DCF Parameters Configuration
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

        # Analysis Configuration
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
        """Create comprehensive results display with tabbed interface"""
        self.results_notebook = ttk.Notebook(self.results_pane)
        self.results_notebook.pack(fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        # DCF Summary Tab
        self.summary_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.summary_frame, text="DCF Summary")

        summary_inner = ttk.LabelFrame(self.summary_frame, text="Valuation Results", padding=10)
        summary_inner.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        self.results_text = tk.Text(summary_inner, height=12, font=('Courier', 10), wrap='word', relief='flat')
        scrollbar1 = ttk.Scrollbar(summary_inner, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar1.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        # Cash Flow Projections Table
        cf_frame = ttk.LabelFrame(self.summary_frame, text="Cash Flow Projections", padding=10)
        cf_frame.pack(fill=tk.BOTH, expand=True)

        self.cf_table = ttk.Treeview(cf_frame, columns=("year", "fcf", "pv_fcf"), show='headings', height=6)
        self.cf_table.heading("year", text="Year")
        self.cf_table.heading("fcf", text="Projected FCF (M)")
        self.cf_table.heading("pv_fcf", text="Present Value (M)")
        self.cf_table.column("year", width=80, anchor='center')
        self.cf_table.column("fcf", width=150, anchor='e')
        self.cf_table.column("pv_fcf", width=150, anchor='e')
        self.cf_table.pack(fill=tk.BOTH, expand=True)

        # Additional Analysis Tabs
        self.cf_chart_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.cf_chart_frame, text="Cash Flow Chart")

        self.sensitivity_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.sensitivity_frame, text="Sensitivity Analysis")

        sens_inner = ttk.LabelFrame(self.sensitivity_frame, text="Sensitivity to Key Variables", padding=10)
        sens_inner.pack(fill=tk.BOTH, expand=True)

        self.sensitivity_table = ttk.Treeview(sens_inner, columns=("variable", "adjustment", "value", "change"),
                                              show='headings', height=15)
        self.sensitivity_table.heading("variable", text="Variable")
        self.sensitivity_table.heading("adjustment", text="Adjustment")
        self.sensitivity_table.heading("value", text="Intrinsic Value")
        self.sensitivity_table.heading("change", text="% Change")
        self.sensitivity_table.column("variable", width=120)
        self.sensitivity_table.column("adjustment", width=100, anchor='center')
        self.sensitivity_table.column("value", width=120, anchor='e')
        self.sensitivity_table.column("change", width=100, anchor='e')

        scrollbar2 = ttk.Scrollbar(sens_inner, orient="vertical", command=self.sensitivity_table.yview)
        self.sensitivity_table.configure(yscrollcommand=scrollbar2.set)
        self.sensitivity_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

        self.sens_chart_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.sens_chart_frame, text="Sensitivity Chart")

        # Scenario Analysis Components
        self.scenario_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.scenario_frame, text="Scenario Analysis")

        scenario_inner = ttk.LabelFrame(self.scenario_frame, text="Bear/Base/Bull Case Analysis", padding=10)
        scenario_inner.pack(fill=tk.BOTH, expand=True)

        self.scenario_table = ttk.Treeview(scenario_inner,
                                           columns=("scenario", "intrinsic", "upside", "growth", "wacc", "terminal"),
                                           show='headings', height=10)
        self.scenario_table.heading("scenario", text="Scenario")
        self.scenario_table.heading("intrinsic", text="Intrinsic Value")
        self.scenario_table.heading("upside", text="Upside %")
        self.scenario_table.heading("growth", text="Growth Rate")
        self.scenario_table.heading("wacc", text="WACC")
        self.scenario_table.heading("terminal", text="Terminal Growth")

        for col in ["scenario", "intrinsic", "upside", "growth", "wacc", "terminal"]:
            self.scenario_table.column(col, width=110, anchor='center')

        self.scenario_table.pack(fill=tk.BOTH, expand=True)

        self.scenario_chart_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.scenario_chart_frame, text="Scenario Chart")

        self.results_text.insert(tk.END, "Enter a ticker symbol and click 'Fetch Data' to begin analysis.")

    def _fetch_data_threaded(self):
        """Initialize threaded data fetching process"""
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
        """Execute data fetching in background thread"""
        try:
            params = self.data_processor.fetch_yahoo_data(ticker)
            self.after(0, self._update_params_from_fetch, params)
        except Exception as e:
            self.after(0, messagebox.showerror, "Error", f"Failed to fetch data for {ticker}:\n{e}")
        finally:
            self.after(0, self._reset_fetch_button)

    def _update_params_from_fetch(self, params):
        """Update interface with fetched financial data"""
        self.dcf_params['enterprise_value'].set(params['enterprise_value'])
        self.dcf_params['debt'].set(params['debt'])
        self.dcf_params['cash'].set(params['cash'])
        self.dcf_params['shares_outstanding'].set(params['shares_outstanding'])
        self.dcf_params['last_fcf'].set(params['last_fcf'])
        self.dcf_params['growth_rate'].set(params['growth_rate'] * 100)

        self.results_text.delete(1.0, tk.END)

        debug_info = (f"Data for {self.ticker_var.get()} loaded successfully.\n"
                      f"Industry: {params['industry']}\n"
                      f"Enterprise Value: ${params['enterprise_value']:.2f}M\n"
                      f"Last FCF: ${params['last_fcf']:.2f}M\n"
                      f"Growth Rate: {params['growth_rate']:.2%}\n"
                      f"Debt: ${params['debt']:.2f}M\n"
                      f"Cash: ${params['cash']:.2f}M\n"
                      f"Shares Outstanding: {params['shares_outstanding']:.2f}M\n"
                      "Parameters loaded. Click 'Calculate DCF' to proceed.")

        self.results_text.insert(tk.END, debug_info)
        self.industry = params['industry']

    def _reset_fetch_button(self):
        """Reset fetch button to normal state"""
        self.fetch_button.config(state="normal", text="Fetch Data")

    def calculate_dcf(self):
        """Execute comprehensive DCF analysis with advanced analytics"""
        try:
            params_values = {name: var.get() for name, var in self.dcf_params.items()}
            params_values['growth_rate'] /= 100
            params_values['wacc'] /= 100
            params_values['terminal_growth_rate'] /= 100
            params_values['industry'] = self.industry

            years = self.projection_years_var.get()

            model = DiscountedCashFlowModel(**params_values)
            intrinsic_value = model.calculate_intrinsic_value(years)
            current_price = model.calculate_implied_share_price()

            projected_fcf = model.project_free_cash_flows(years)
            terminal_value = model.calculate_terminal_value(projected_fcf[-1])
            intrinsic_ev = model.calculate_present_value(projected_fcf, terminal_value)

            self._display_dcf_results(model, intrinsic_value, current_price, intrinsic_ev, terminal_value, years)
            self._update_cf_table(projected_fcf, model.wacc, terminal_value, years)

            sensitivity_results = model.sensitivity_analysis(years)
            self._update_sensitivity_table(sensitivity_results)

            scenario_results = model.scenario_analysis(years)
            self._update_scenario_table(scenario_results)

            self._update_charts(projected_fcf, terminal_value, model.wacc, years,
                                sensitivity_results, scenario_results)

        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred during calculation:\n{e}")

    def _update_charts(self, projected_fcf, terminal_value, wacc, years, sensitivity_results, scenario_results):
        """Generate and display professional visualization charts"""
        try:
            for widget in self.cf_chart_frame.winfo_children():
                widget.destroy()
            for widget in self.sens_chart_frame.winfo_children():
                widget.destroy()
            for widget in self.scenario_chart_frame.winfo_children():
                widget.destroy()

            cf_canvas = self.charts.create_cash_flow_chart(
                self.cf_chart_frame, projected_fcf, terminal_value, wacc, years)
            cf_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            sens_canvas = self.charts.create_sensitivity_chart(
                self.sens_chart_frame, sensitivity_results)
            sens_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            scenario_canvas = self.charts.create_scenario_chart(
                self.scenario_chart_frame, scenario_results)
            scenario_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Chart generation error: {e}")

    def _update_sensitivity_table(self, sensitivity_results):
        """Populate sensitivity analysis data table"""
        for item in self.sensitivity_table.get_children():
            self.sensitivity_table.delete(item)

        variable_names = {
            'growth_rate': 'FCF Growth Rate',
            'wacc': 'WACC',
            'terminal_growth_rate': 'Terminal Growth'
        }

        for variable, results in sensitivity_results.items():
            display_name = variable_names.get(variable, variable)
            for result in results:
                adjustment = result['adjustment']
                value = result['intrinsic_value']
                change = result['percentage_change']

                if variable == 'growth_rate':
                    adj_display = f"{adjustment:+.1%}"
                elif variable == 'wacc':
                    adj_display = f"{adjustment:+.1%}"
                else:
                    adj_display = f"{adjustment:+.2%}"

                self.sensitivity_table.insert("", "end", values=(
                    display_name,
                    adj_display,
                    f"${value:.2f}",
                    f"{change:+.1f}%"
                ))

    def _update_scenario_table(self, scenario_results):
        """Populate scenario analysis comparison table"""
        for item in self.scenario_table.get_children():
            self.scenario_table.delete(item)

        for scenario, results in scenario_results.items():
            if 'error' in results:
                self.scenario_table.insert("", "end", values=(
                    scenario,
                    "ERROR",
                    results['error'],
                    f"{results['growth_rate']:.1%}",
                    f"{results['wacc']:.1%}",
                    f"{results['terminal_growth_rate']:.1%}"
                ))
            else:
                self.scenario_table.insert("", "end", values=(
                    scenario,
                    f"${results['intrinsic_value']:.2f}",
                    f"{results['upside_percentage']:+.1f}%",
                    f"{results['growth_rate']:.1%}",
                    f"{results['wacc']:.1%}",
                    f"{results['terminal_growth_rate']:.1%}"
                ))

    def _display_dcf_results(self, model, intrinsic_value, current_price, enterprise_value, terminal_value, years):
        """Format and display comprehensive valuation results"""
        self.results_text.delete(1.0, tk.END)
        upside = ((intrinsic_value - current_price) / current_price * 100) if current_price else 0
        summary = "UNDERVALUED" if intrinsic_value > current_price else "OVERVALUED"

        results_string = f"""
=== DCF VALUATION ANALYSIS: {self.ticker_var.get()} ===

VALUATION SUMMARY:
Intrinsic Value per Share: ${intrinsic_value:10.2f}
Current Implied Price:     ${current_price:10.2f}
Upside/Downside:           {upside:10.1f}%
Investment Thesis:         {summary} by ${abs(intrinsic_value - current_price):.2f}

ENTERPRISE VALUATION (Millions USD):
Intrinsic Enterprise Value: ${enterprise_value:10,.0f}
Terminal Value (PV):       ${terminal_value / ((1 + model.wacc) ** years):10,.0f}
Intrinsic Equity Value:    ${enterprise_value - model.debt + model.cash:10,.0f}

MODELING ASSUMPTIONS:
FCF Growth Rate:           {model.growth_rate:.2%}
Weighted Avg Cost Capital: {model.wacc:.2%}
Terminal Growth Rate:      {model.terminal_growth_rate:.2%}
Projection Period:         {years} years
"""
        self.results_text.insert(tk.END, results_string)

    def _update_cf_table(self, projected_fcf, wacc, terminal_value, years):
        """Update cash flow projections table with calculated values"""
        for item in self.cf_table.get_children():
            self.cf_table.delete(item)

        for i, fcf in enumerate(projected_fcf):
            year = i + 1
            pv_fcf = fcf / ((1 + wacc) ** year)
            self.cf_table.insert("", "end", values=(f"Year {year}", f"${fcf:,.1f}M", f"${pv_fcf:,.1f}M"))

        pv_terminal = terminal_value / ((1 + wacc) ** years)
        self.cf_table.insert("", "end", values=("Terminal", f"${terminal_value:,.1f}M", f"${pv_terminal:,.1f}M"))