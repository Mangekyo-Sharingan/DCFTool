# Financial Analysis Dashboard - Vibe-code ed.

A professional-grade financial analysis platform featuring comprehensive DCF valuation tools with plans for expanded financial modeling capabilities.

## 🚀 Features

### Current Tools
- **DCF Valuation Tool**: Professional discounted cash flow analysis with sensitivity testing and scenario modeling
  - Multi-year cash flow projections (5, 10, or 15 years)
  - Real-time company data fetching via stock ticker
  - Interactive charts and visualizations
  - Comprehensive sensitivity analysis
  - Professional reporting and detailed projections table

### Platform Features
- **Dark Mode**: Toggle-able dark/light theme with system preference detection
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Professional UI**: Clean, modern interface built with Tailwind CSS
- **Real-time Charts**: Interactive visualizations using Chart.js
- **RESTful API**: Backend API for financial calculations and data processing

### Coming Soon
- Portfolio Analysis & Optimization
- Monte Carlo Simulation
- Options Pricing (Black-Scholes & Binomial Models)
- Credit Risk Assessment
- Bond Pricing & Fixed Income Analysis

## 🏗️ Architecture

### Frontend (Astro + Tailwind CSS)
- **Dashboard**: `/` - Main landing page with tool overview
- **DCF Tool**: `/dcf-tool` - Dedicated DCF analysis interface
- **Dark Mode**: Global theme toggle with localStorage persistence
- **Responsive**: Mobile-first design with dark mode support

### Backend (Python + Flask)
- **API Endpoints**: RESTful API for financial calculations
- **Data Processing**: Real-time company data fetching and processing
- **DCF Engine**: Professional-grade valuation calculations
- **Error Handling**: Comprehensive error handling and validation

### Key Components
```
├── frontend/                 # Astro frontend application
│   ├── src/
│   │   ├── layouts/         # Layout components with dark mode
│   │   └── pages/           # Dashboard and tool pages
├── models/                  # Financial calculation models
├── data/                    # Data processing and API integration
├── gui/                     # Chart generation and visualization
└── tests/                   # Comprehensive test suite
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd DCFTool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📊 DCF Tool Usage

### Basic Workflow
1. **Access Tool**: Navigate to `/dcf-tool` from the dashboard
2. **Company Data**: Enter stock ticker and fetch company data automatically
3. **Financial Inputs**: Provide required financial parameters:
   - Shares Outstanding (required)
   - Last Free Cash Flow (required)
   - Growth Rate (required)
   - WACC - Weighted Average Cost of Capital (required)
   - Terminal Growth Rate (required)
   - Optional: Enterprise Value, Debt, Cash & Equivalents
4. **Calculate**: Run DCF analysis to get intrinsic valuation
5. **Review Results**: Analyze charts, sensitivity data, and detailed projections

### Key Metrics Calculated
- **Intrinsic Value per Share**: Based on discounted future cash flows
- **Upside/Downside**: Comparison with current market price
- **Cash Flow Projections**: Multi-year forward-looking estimates
- **Sensitivity Analysis**: Impact of WACC variations on valuation
- **Present Value Breakdown**: Detailed year-by-year analysis

## 🎨 Dark Mode

The platform features a comprehensive dark mode implementation:
- **Global Toggle**: Fixed-position button accessible from any page
- **Theme Persistence**: Preferences saved in localStorage
- **System Detection**: Automatically detects OS dark mode preference
- **Dynamic Charts**: Chart colors adapt to current theme
- **Smooth Transitions**: All elements transition smoothly between themes

## 🔧 API Endpoints

### Company Data
```http
GET /api/company-data/{ticker}
```
Fetches real-time company financial data for a given stock ticker.

### DCF Calculation
```http
POST /api/calculate-dcf
Content-Type: application/json

{
  "ticker": "AAPL",
  "shares_outstanding": 15000,
  "last_fcf": 95000,
  "growth_rate": 5.0,
  "wacc": 8.0,
  "terminal_growth_rate": 2.0,
  "projection_years": 10
}
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run all tests
python tests/run_all.py

# Run specific test categories
python -m pytest tests/test_dcf_model.py
python -m pytest tests/test_data_processor.py
python -m pytest tests/test_integration.py
```

## 📈 Future Roadmap

### Phase 2: Portfolio Analysis
- Modern Portfolio Theory implementation
- Risk-return optimization
- Efficient frontier analysis
- Portfolio performance tracking

### Phase 3: Advanced Modeling
- Monte Carlo simulation engine
- Options pricing models (Black-Scholes, Binomial)
- Credit risk modeling and scoring
- Fixed income analysis tools

## 📞 Support

For questions, feature requests, or bug reports, please open an issue on GitHub.

---

**Built with AI️ and vibes for hobby investors**
