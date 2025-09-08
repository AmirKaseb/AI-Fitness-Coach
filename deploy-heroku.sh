#!/bin/bash

# Heroku Deployment Script
echo "🚀 Deploying GymJam AI to Heroku..."

# Install Heroku CLI if not installed
if ! command -v heroku &> /dev/null; then
    echo "Please install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku
echo "Logging into Heroku..."
heroku login

# Create Heroku app
echo "Creating Heroku app..."
read -p "Enter your app name (or press Enter for auto-generated): " app_name
if [ -z "$app_name" ]; then
    heroku create
else
    heroku create $app_name
fi

# Add buildpacks for Python and OpenCV
echo "Adding buildpacks..."
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# Set environment variables
echo "Setting environment variables..."
heroku config:set FLASK_ENV=production

# Deploy to Heroku
echo "Deploying to Heroku..."
git add .
git commit -m "Deploy GymJam AI to Heroku"
git push heroku main

echo "✅ Deployment complete!"
echo "Your app will be available at: https://your-app-name.herokuapp.com"
