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
from models.dcf_model import DiscountedCashFlowModel
from data.data_processor import DataProcessor
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
    "http://localhost",       # Docker nginx proxy
    "http://localhost:80",    # Docker nginx proxy with port
    "*"                       # Allow all origins for development (remove in production)
], supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])

# Initialize components
data_processor = DataProcessor()

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

@app.route('/api/company-data/<ticker>', methods=['GET'])
def get_company_data(ticker):
    """Fetch company financial data by ticker symbol (GET endpoint for frontend)"""
    try:
        ticker = ticker.upper()
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400

        # Fetch data using the existing data processor
        data = data_processor.fetch_yahoo_data(ticker)

        # Format the response to match what the frontend expects
        response = {
            'ticker': ticker,
            'success': True
        }

        # Add the financial data fields that the frontend looks for
        if data:
            response.update({
                'shares_outstanding': data.get('shares_outstanding'),
                'debt': data.get('debt'),
                'cash': data.get('cash'),
                'enterprise_value': data.get('enterprise_value'),
                'industry': data.get('industry'),
                'last_fcf': data.get('last_fcf'),  # Use the correct field name from data processor
                'market_cap': data.get('market_cap'),
                'current_price': data.get('current_price')
            })

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error fetching company data for {ticker}: {str(e)}")
        return jsonify({
            'error': f'Failed to fetch data for {ticker}',
            'success': False,
            'ticker': ticker
        }), 500

@app.route('/api/calculate-dcf', methods=['POST'])
def calculate_dcf():
    """Calculate DCF valuation"""
    try:
        if not request.json:
            return jsonify({'error': 'Request body must be JSON'}), 400

        params = request.json

        # Add debug logging to see what data we're receiving
        logger.info(f"DEBUG: Received DCF calculation request with params: {params}")

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

        logger.info(f"DEBUG: Processed parameters - last_fcf={last_fcf}, shares_outstanding={shares_outstanding}, growth_rate={growth_rate}")

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

        logger.info(f"DEBUG: DCF model created successfully")

        # Calculate results with individual error handling
        try:
            intrinsic_value = dcf_model.calculate_intrinsic_value(years=projection_years)
            logger.info(f"DEBUG: Intrinsic value calculated: {intrinsic_value}")
        except Exception as e:
            logger.error(f"ERROR in calculate_intrinsic_value: {str(e)}")
            raise

        try:
            projections_data = dcf_model.project_cash_flows(years=projection_years)
            logger.info(f"DEBUG: Projections calculated successfully")
        except Exception as e:
            logger.error(f"ERROR in project_cash_flows: {str(e)}")
            raise

        try:
            sensitivity = dcf_model.sensitivity_analysis(years=projection_years)
            logger.info(f"DEBUG: Sensitivity analysis completed")
        except Exception as e:
            logger.error(f"ERROR in sensitivity_analysis: {str(e)}")
            raise

        try:
            scenarios = dcf_model.scenario_analysis(years=projection_years)
            logger.info(f"DEBUG: Scenario analysis completed")
        except Exception as e:
            logger.error(f"ERROR in scenario_analysis: {str(e)}")
            raise

        # Format projections as array of objects for frontend
        projections = []
        if projections_data and 'projected_fcf' in projections_data:
            projected_fcf = projections_data['projected_fcf']
            present_values = projections_data.get('present_values', [])
            years_list = projections_data.get('years', list(range(1, projection_years + 1)))

            for i, year in enumerate(years_list):
                if i < len(projected_fcf) and i < len(present_values):
                    fcf = projected_fcf[i]
                    present_value = present_values[i]
                    # Calculate PV factor properly: PV = FCF * PV_factor, so PV_factor = PV / FCF
                    pv_factor = (1 + wacc) ** -(year) if wacc > 0 else 1

                    projections.append({
                        'year': year,
                        'fcf': round(fcf, 2),
                        'pv_factor': round(pv_factor, 4),
                        'present_value': round(present_value, 2)
                    })

        # Format sensitivity analysis for frontend (simple array of values)
        sensitivity_values = []
        if sensitivity and 'wacc' in sensitivity:
            wacc_results = sensitivity['wacc']
            # Get the intrinsic values for WACC -1%, base, +1%
            if len(wacc_results) >= 3:
                # Extract values safely and ensure they're valid numbers
                try:
                    val1 = wacc_results[0]['intrinsic_value'] if wacc_results[0]['intrinsic_value'] > 0 else 0
                    val2 = wacc_results[2]['intrinsic_value'] if len(wacc_results) > 2 and wacc_results[2]['intrinsic_value'] > 0 else 0
                    val3 = wacc_results[4]['intrinsic_value'] if len(wacc_results) > 4 and wacc_results[4]['intrinsic_value'] > 0 else wacc_results[-1]['intrinsic_value'] if wacc_results[-1]['intrinsic_value'] > 0 else 0

                    sensitivity_values = [round(val1, 2), round(val2, 2), round(val3, 2)]
                except (KeyError, IndexError, TypeError):
                    sensitivity_values = [0, 0, 0]

        # Fallback if no sensitivity data
        if not sensitivity_values:
            sensitivity_values = [0, 0, 0]

        # Get current price for comparison (if available from earlier fetch)
        current_price = None
        if ticker:
            try:
                company_data = data_processor.fetch_yahoo_data(ticker)
                current_price = company_data.get('current_price') or company_data.get('price') if company_data else None
            except:
                pass  # Current price is optional

        return jsonify({
            'success': True,
            'intrinsic_value': round(intrinsic_value, 2),
            'current_price': current_price,
            'projections': projections,
            'sensitivity_analysis': sensitivity_values,
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
        })

    except Exception as e:
        logger.error(f"Error in DCF calculation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'API endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
