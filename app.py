"""
Flask app for the DCF valuation tool.
"""

import os
from flask import Flask, render_template, request, jsonify
from models.dcf_model import DCFModel
from data.data_processor import DataProcessor
from charts import DCFCharts

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-me")

data_processor = DataProcessor()
charts = DCFCharts()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/fetch-data", methods=["POST"])
def fetch_data():
    """Pull financials from Yahoo Finance for the given ticker."""
    try:
        ticker = request.json.get("ticker", "").upper()
        if not ticker:
            return jsonify({"error": "Ticker symbol required"}), 400

        data = data_processor.fetch_yahoo_data(ticker)
        return jsonify({"success": True, "data": data, "ticker": ticker})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/calculate-dcf", methods=["POST"])
def calculate_dcf():
    """Run DCF valuation with the supplied parameters."""
    try:
        p = request.json

        model = DCFModel(
            enterprise_value=p.get("enterprise_value", 0),
            debt=p.get("debt", 0),
            cash=p.get("cash", 0),
            shares_outstanding=p.get("shares_outstanding", 0),
            last_fcf=p.get("last_fcf", 0),
            growth_rate=p.get("growth_rate", 5) / 100,
            wacc=p.get("wacc", 8) / 100,
            terminal_growth_rate=p.get("terminal_growth_rate", 2) / 100,
            industry=p.get("industry", "N/A"),
        )

        years = p.get("projection_years", 5)

        return jsonify(
            {
                "success": True,
                "results": {
                    "intrinsic_value": model.intrinsic_value(years),
                    "projections": model.project_cash_flows(years),
                    "sensitivity": model.sensitivity_analysis(years),
                    "scenarios": model.scenario_analysis(years),
                },
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-charts", methods=["POST"])
def generate_charts():
    """Return base64-encoded chart PNGs."""
    try:
        data = request.json
        result = {}

        if data.get("projections"):
            result["projections"] = charts.create_projections_chart(data["projections"])
        if data.get("sensitivity"):
            result["sensitivity"] = charts.create_sensitivity_chart(data["sensitivity"])
        if data.get("scenarios"):
            result["scenarios"] = charts.create_scenarios_chart(data["scenarios"])

        return jsonify({"success": True, "charts": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
