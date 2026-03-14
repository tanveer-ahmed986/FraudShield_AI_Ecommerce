#!/usr/bin/env bash
# Render build script for fraud detection backend

set -o errexit  # Exit on error

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install .

echo "📁 Creating directories..."
mkdir -p models data

echo "🔍 Checking for model files..."
if [ -f "models/v6.0_model.pkl" ]; then
    echo "✅ Model v6.0 found"
else
    echo "⚠️  No pre-trained model found. Model will need to be trained after deployment."
fi

echo "🗄️ Running database migrations..."
# Note: Alembic migrations can be added here if needed
# alembic upgrade head

echo "✅ Build complete!"
