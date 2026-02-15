#!/bin/bash
# Setup database with CSV data for Render deployment

echo "🔧 Setting up database..."

# Run migrations
alembic upgrade head

# Load CSV data
echo "📊 Loading customer data from CSV..."
python load_csv_data.py

echo "✅ Database setup complete!"
