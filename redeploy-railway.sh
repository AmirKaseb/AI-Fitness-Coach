#!/bin/bash

echo "🚀 Redeploying GymJam AI to Railway..."

# Remove Dockerfile to force Nixpacks
echo "📁 Removing Dockerfile to force Nixpacks usage..."
rm -f Dockerfile

# Add all changes
echo "📦 Adding all changes..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Fix Railway deployment - use Nixpacks instead of Docker"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Deployment triggered! Railway will now use Nixpacks instead of Docker."
echo "🔗 Check your Railway dashboard for deployment progress."
echo "📱 Your app will be available at: https://your-app-name.railway.app"
