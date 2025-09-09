#!/bin/bash

# GymJam AI WebRTC Railway Deployment Script
echo "🚀 Starting GymJam AI WebRTC deployment to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "🔐 Checking Railway authentication..."
railway whoami || railway login

# Deploy to Railway
echo "📦 Deploying to Railway..."
railway up

echo "✅ Deployment initiated! Check your Railway dashboard for progress."
echo "🌐 Your app will be available at: https://web-production-4229e.up.railway.app"