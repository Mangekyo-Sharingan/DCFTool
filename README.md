# DCF Valuation Tool - Web Edition

## Overview
A comprehensive Flask web application for discounted cash flow (DCF) valuation of publicly traded companies. This professional-grade tool provides advanced financial analysis capabilities through an intuitive web interface.

## Features
- **Real-time Data Fetching**: Integrates with Yahoo Finance API for live financial data
- **DCF Calculations**: Professional-grade valuation models with configurable parameters
- **Interactive Charts**: Dynamic visualizations for cash flow projections, sensitivity analysis, and scenario modeling
- **Responsive Design**: Modern web interface optimized for desktop and mobile devices
- **Docker Support**: Containerized deployment for easy scaling and distribution

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application at http://localhost:5000
```

### Production Deployment with Nginx
```bash
# Run with nginx reverse proxy
docker-compose --profile production up --build

# Access the application at http://localhost
```

## API Endpoints
- `GET /` - Main application interface
- `POST /api/fetch-data` - Fetch financial data for ticker symbol
- `POST /api/calculate-dcf` - Calculate DCF valuation
- `POST /api/generate-charts` - Generate analysis charts

## Docker Images
The application includes optimized Docker configuration:
- Multi-stage build for reduced image size
- Non-root user for enhanced security
- Health checks for monitoring
- Production-ready with gunicorn WSGI server

## Technology Stack
- **Backend**: Flask, Python 3.9+
- **Data**: Yahoo Finance API, Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Deployment**: Docker, Gunicorn, Nginx

## License
MIT License - Professional Edition
