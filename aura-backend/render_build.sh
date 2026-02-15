#!/bin/bash
set -e

echo "🚀 Starting Render build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if database exists
if [ ! -f "aura_dev.db" ]; then
    echo "📊 Database not found. Creating and seeding..."
    
    # Load CSV data
    echo "📥 Loading customer data from CSV..."
    python load_csv_data.py
    
    # Run predictions
    echo "🤖 Running ML predictions for all customers..."
    python predict_all_customers.py
    
    echo "✅ Database setup complete!"
else
    echo "✅ Database already exists, skipping setup"
fi

echo "🎉 Build complete!"
