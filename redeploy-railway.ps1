# GymJam AI WebRTC Railway Deployment Script (PowerShell)
Write-Host "🚀 Starting GymJam AI WebRTC deployment to Railway..." -ForegroundColor Green

# Check if railway CLI is installed
try {
    railway --version | Out-Null
    Write-Host "✅ Railway CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Railway CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "npm install -g @railway/cli" -ForegroundColor Yellow
    exit 1
}

# Login to Railway (if not already logged in)
Write-Host "🔐 Checking Railway authentication..." -ForegroundColor Blue
try {
    railway whoami | Out-Null
    Write-Host "✅ Already authenticated with Railway" -ForegroundColor Green
} catch {
    Write-Host "🔑 Please login to Railway..." -ForegroundColor Yellow
    railway login
}

# Deploy to Railway
Write-Host "📦 Deploying to Railway..." -ForegroundColor Blue
railway up

Write-Host "✅ Deployment initiated! Check your Railway dashboard for progress." -ForegroundColor Green
Write-Host "🌐 Your app will be available at: https://web-production-4229e.up.railway.app" -ForegroundColor Cyan
