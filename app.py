"""
DCF Valuation Tool - Flask Web Application

A comprehensive financial analysis web application for discounted cash flow
valuation of publicly traded companies.

Author: DCF Development Team
Version: 2.0.0 (Web Edition)
License: MIT
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import io
import base64
from models.dcf_model import DiscountedCashFlowModel
from data.data_processor import DataProcessor
from gui.charts import DCFCharts

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dcf-valuation-tool-secret-key'

# Initialize components
data_processor = DataProcessor()
charts = DCFCharts()

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/fetch-data', methods=['POST'])
def fetch_data():
    """Fetch financial data for a given ticker"""
    try:
        ticker = request.json.get('ticker', '').upper()
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400

        data = data_processor.fetch_yahoo_data(ticker)
        return jsonify({
            'success': True,
            'data': data,
            'ticker': ticker
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate-dcf', methods=['POST'])
def calculate_dcf():
    """Calculate DCF valuation"""
    try:
        params = request.json

        # Extract parameters
        enterprise_value = params.get('enterprise_value', 0)
        debt = params.get('debt', 0)
        cash = params.get('cash', 0)
        shares_outstanding = params.get('shares_outstanding', 0)
        last_fcf = params.get('last_fcf', 0)
        growth_rate = params.get('growth_rate', 5) / 100  # Convert percentage
        wacc = params.get('wacc', 8) / 100  # Convert percentage
        terminal_growth_rate = params.get('terminal_growth_rate', 2) / 100  # Convert percentage
        projection_years = params.get('projection_years', 5)
        industry = params.get('industry', 'N/A')

        # Create DCF model
        dcf_model = DiscountedCashFlowModel(
            enterprise_value=enterprise_value,
            debt=debt,
            cash=cash,
            shares_outstanding=shares_outstanding,
            last_fcf=last_fcf,
            growth_rate=growth_rate,
            wacc=wacc,
            terminal_growth_rate=terminal_growth_rate,
            industry=industry
        )

        # Calculate results
        intrinsic_value = dcf_model.calculate_intrinsic_value(years=projection_years)
        projections = dcf_model.project_cash_flows(years=projection_years)
        sensitivity = dcf_model.sensitivity_analysis(years=projection_years)
        scenarios = dcf_model.scenario_analysis(years=projection_years)

        return jsonify({
            'success': True,
            'results': {
                'intrinsic_value': intrinsic_value,
                'projections': projections,
                'sensitivity': sensitivity,
                'scenarios': scenarios
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-charts', methods=['POST'])
def generate_charts():
    """Generate charts for DCF analysis"""
    try:
        data = request.json
        projections = data.get('projections', {})
        sensitivity = data.get('sensitivity', {})
        scenarios = data.get('scenarios', {})

        # Generate charts and convert to base64
        charts_data = {}

        if projections:
            chart_img = charts.create_projections_chart(projections)
            charts_data['projections'] = chart_img

        if sensitivity:
            chart_img = charts.create_sensitivity_chart(sensitivity)
            charts_data['sensitivity'] = chart_img

        if scenarios:
            chart_img = charts.create_scenarios_chart(scenarios)
            charts_data['scenarios'] = chart_img

        return jsonify({
            'success': True,
            'charts': charts_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
