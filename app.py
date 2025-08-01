"""
DCF Valuation Tool - Flask API Backend

A REST API for discounted cash flow valuation calculations.
Serves as the backend for the modern Astro frontend.

Author: DCF Development Team
Version: 3.0.0 (API Edition)
License: MIT
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import io
import base64
from models.dcf_model import DiscountedCashFlowModel
from data.data_processor import DataProcessor
from gui.charts import DCFCharts
from config import config
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Enable CORS for frontend communication
CORS(app, origins=[
    "http://localhost:3000",  # Astro dev server
    "http://localhost:4321",  # Alternative Astro port
    "http://frontend:3000",   # Docker frontend service
    "http://localhost:4000",  # Additional dev port
], supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])

# Initialize components
data_processor = DataProcessor()
charts = DCFCharts()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancer and monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'DCF API Backend',
        'version': '3.0.0'
    })

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
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate-dcf', methods=['POST'])
def calculate_dcf():
    """Calculate DCF valuation"""
    try:
        if not request.json:
            return jsonify({'error': 'Request body must be JSON'}), 400

        params = request.json

        # Validate required parameters
        required_fields = ['shares_outstanding', 'last_fcf', 'growth_rate', 'wacc', 'terminal_growth_rate']
        for field in required_fields:
            if field not in params:
                return jsonify({'error': f'Missing required field: {field}'}), 400

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
        ticker = params.get('ticker', '').upper()

        # Validate inputs
        if shares_outstanding <= 0:
            return jsonify({'error': 'Shares outstanding must be positive'}), 400
        if wacc <= terminal_growth_rate:
            return jsonify({'error': 'WACC must be greater than terminal growth rate'}), 400

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
            'data': {
                'intrinsic_value': round(intrinsic_value, 2),
                'projections': projections,
                'sensitivity': sensitivity,
                'scenarios': scenarios,
                'input_parameters': {
                    'ticker': ticker,
                    'enterprise_value': enterprise_value,
                    'debt': debt,
                    'cash': cash,
                    'shares_outstanding': shares_outstanding,
                    'last_fcf': last_fcf,
                    'growth_rate': growth_rate * 100,
                    'wacc': wacc * 100,
                    'terminal_growth_rate': terminal_growth_rate * 100,
                    'projection_years': projection_years,
                    'industry': industry
                }
            }
        })

    except Exception as e:
        logger.error(f"Error in DCF calculation: {str(e)}")
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
        logger.error(f"Error generating charts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'API endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
