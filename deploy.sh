#!/bin/bash
# Quick deployment script for fraud detection system

set -e

echo "🚀 Fraud Detection System - Production Deployment"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Production deployment setup"
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "❌ No git remote configured."
    echo "Please create a GitHub repository and run:"
    echo "  git remote add origin https://github.com/YOUR-USERNAME/fraud-detection-system.git"
    echo "  git push -u origin main"
    exit 1
fi

echo "✅ Git repository ready"
echo ""

# Frontend deployment check
echo "🎨 Frontend Deployment (Vercel)"
echo "------------------------------"
cd frontend

if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI not installed."
    echo "Install with: npm install -g vercel"
    echo "Or deploy via Vercel Dashboard: https://vercel.com/dashboard"
else
    echo "✅ Vercel CLI found"
    echo "Run 'vercel --prod' to deploy frontend"
fi

cd ..
echo ""

# Backend deployment check
echo "⚙️  Backend Deployment (Render)"
echo "------------------------------"
echo "1. Push code to GitHub:"
echo "   git push origin main"
echo ""
echo "2. Create Render Web Service:"
echo "   https://dashboard.render.com/new/web"
echo ""
echo "3. Configure:"
echo "   - Root Directory: backend"
echo "   - Build Command: ./build.sh"
echo "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "4. Add Environment Variables (see backend/.env.production)"
echo ""

# Database setup check
echo "🗄️  Database Setup (Supabase)"
echo "----------------------------"
echo "1. Create project: https://app.supabase.com"
echo "2. Copy connection string from: Project Settings > Database"
echo "3. Add to Render environment variables"
echo ""

# WooCommerce plugin
echo "🛒 WooCommerce Plugin"
echo "--------------------"
if [ -f "plugin/woo-fraud-detect.zip" ]; then
    echo "✅ Plugin package ready: plugin/woo-fraud-detect.zip"
    echo "   Upload to WordPress: Plugins > Add New > Upload"
else
    echo "❌ Plugin not packaged yet"
    echo "   Run: cd plugin && zip -r woo-fraud-detect.zip woo-fraud-detect/"
fi
echo ""

echo "📚 Full deployment guide: DEPLOYMENT.md"
echo ""
echo "🎉 Ready to deploy! Follow the steps above or see DEPLOYMENT.md"
