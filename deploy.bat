@echo off
REM Windows deployment script for DCF Valuation Tool

echo 🚀 Starting DCF Valuation Tool deployment...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Build and start the application
echo 📦 Building Docker images...
docker-compose build

echo 🌐 Starting DCF Valuation Tool...
docker-compose up -d

echo ✅ DCF Valuation Tool is now running!
echo 🔗 Access the application at: http://localhost:5000
echo.
echo 📊 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
