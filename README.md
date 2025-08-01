# DCF Valuation Tool - Modern Full-Stack Edition

## 🏗️ Architecture Overview
A modern, scalable DCF valuation platform built with:
- **Frontend**: Astro + Tailwind CSS (Node.js)
- **Backend**: Flask REST API (Python)
- **Proxy**: Nginx reverse proxy
- **Deployment**: Docker containers with production security

## ✨ Features
- **Real-time Market Data**: Live stock price fetching from Yahoo Finance API
- **Professional DCF Calculations**: Industry-standard valuation models with configurable parameters
- **Interactive Visualizations**: Dynamic charts for cash flow projections, sensitivity analysis, and scenario modeling
- **Modern UI/UX**: Responsive design with Tailwind CSS and professional styling
- **Production-Ready**: Secure Docker deployment with Nginx reverse proxy

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

## 🐳 Docker Deployment (Recommended)

### Production Deployment
```bash
# Stop any existing containers
docker-compose down

# Build and start all services
docker-compose up --build -d

# Access the application at http://localhost
```

### Check Service Status
```bash
# View all container status
docker-compose ps

# View real-time logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f nginx
```

### Stop Services
```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (clean reset)
docker-compose down -v
```

## 💻 Local Development

### Backend (Flask API)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run Flask API (port 5000)
python app.py

# API will be available at http://localhost:5000/api
```

### Frontend (Astro)
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Run Astro development server (port 3000)
npm run dev

# Frontend will be available at http://localhost:3000
```

## 🔧 Architecture Details

### Service Communication
- **Nginx** (Port 80/443) → Routes traffic to appropriate services
- **Frontend** (Port 3000) → Astro application serving the UI
- **Backend** (Port 5000) → Flask API handling DCF calculations
- **Internal Network** → Services communicate via Docker network

### API Endpoints
- `GET /api/health` - Health check endpoint
- `POST /api/fetch-data` - Fetch financial data for ticker symbol
- `POST /api/calculate-dcf` - Calculate DCF valuation with sensitivity and scenario analysis
- `POST /api/generate-charts` - Generate analysis charts (server-side rendering)

### Frontend Routes
- `/` - Main DCF calculator interface
- All API calls are proxied through Nginx to the Flask backend

## 🔒 Security Features

### Production Security
- **Non-root containers** with specific user IDs
- **Rate limiting** on API endpoints
- **CORS protection** with allowed origins
- **Security headers** (XSS, CSRF, etc.)
- **No direct port exposure** (only through Nginx)
- **SSL/HTTPS ready** (uncomment in nginx.conf)

### Docker Security
- Multi-stage builds to reduce attack surface
- Minimal base images (Alpine Linux)
- Health checks for monitoring
- Volume management for logs

## 📊 Features in Detail

### DCF Calculation Engine
- **Cash Flow Projections**: 5-20 year configurable projections
- **Terminal Value**: Gordon Growth Model implementation
- **Sensitivity Analysis**: Tornado charts for key variables
- **Scenario Analysis**: Bear/Base/Bull case modeling
- **Real-time Pricing**: Live market data integration

### Modern Frontend
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Chart.js integration for visualizations
- **Real-time Updates**: Dynamic form validation and calculations
- **Professional Styling**: Clean, modern interface with Tailwind CSS
- **Error Handling**: Comprehensive user feedback and error states

## 🛠️ Development Commands

### Docker Development
```bash
# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Scale services (if needed)
docker-compose up --scale backend=2

# Execute commands in running containers
docker-compose exec backend python -c "print('Backend running')"
docker-compose exec frontend npm list
```

### Debugging
```bash
# View detailed logs with timestamps
docker-compose logs -f --timestamps

# Check container resource usage
docker stats $(docker-compose ps -q)

# Enter container shell for debugging
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'production' for production deployment
- `NODE_ENV`: Set to 'production' for optimized frontend builds
- `API_URL`: Backend API URL (configured automatically in Docker)

### Customization
- **Nginx Config**: Edit `nginx.conf` for SSL, domains, or routing changes
- **Frontend Styling**: Modify `frontend/tailwind.config.mjs` for design customization
- **Backend API**: Extend `app.py` for additional endpoints or features

## 📈 Performance

### Optimizations
- **Gzip compression** enabled in Nginx
- **Static asset caching** with long expiry headers
- **Connection pooling** between services
- **Multi-stage Docker builds** for smaller images
- **Asset optimization** in Astro production builds

## 🚨 Troubleshooting

### Common Issues
```bash
# Port conflicts
docker-compose down && docker system prune -f

# Rebuild from scratch
docker-compose down -v
docker system prune -a -f
docker-compose up --build --force-recreate

# Check service health
curl http://localhost/health
curl http://localhost/api/health
```

### Development Issues
```bash
# Frontend not connecting to backend
# Check CORS settings in app.py and API_URL in frontend

# Charts not updating
# Verify chart.js is loaded and data is being passed correctly

# Docker permission issues (Linux/Mac)
sudo chown -R $USER:$USER .
```

## 📝 License
MIT License - See LICENSE file for details

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker deployment
5. Submit a pull request

---

**Note**: This application has been refactored from a Flask monolith to a modern microservices architecture with enhanced security, performance, and scalability.
