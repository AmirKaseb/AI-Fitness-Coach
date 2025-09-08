#!/bin/bash

# Railway Deployment Script
echo "🚀 Deploying GymJam AI to Railway..."

# Install Railway CLI if not installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "Logging into Railway..."
railway login

# Initialize Railway project
echo "Initializing Railway project..."
railway init

# Deploy to Railway
echo "Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "Your app will be available at: https://your-app-name.railway.app"
