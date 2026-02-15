#!/bin/bash
set -e

echo "🚀 Starting AURA Backend on Render..."

# Check if database exists in persistent disk
DISK_PATH="/opt/render/project/src/aura-backend/data"
DB_FILE="$DISK_PATH/aura_dev.db"

if [ -d "$DISK_PATH" ]; then
    echo "📁 Persistent disk found at $DISK_PATH"
    
    # Create symlink to database in persistent disk
    if [ -f "$DB_FILE" ]; then
        echo "✅ Database found in persistent disk"
        ln -sf "$DB_FILE" ./aura_dev.db
    else
        echo "⚠️  Database not found in persistent disk"
        echo "📊 Creating new database..."
        
        # Create database in persistent disk
        python load_csv_data.py
        python predict_all_customers.py
        
        # Move database to persistent disk
        mv ./aura_dev.db "$DB_FILE"
        ln -sf "$DB_FILE" ./aura_dev.db
        
        echo "✅ Database created and moved to persistent disk"
    fi
else
    echo "⚠️  No persistent disk mounted"
    echo "📊 Using ephemeral database (will reset on redeploy)"
    
    if [ ! -f "./aura_dev.db" ]; then
        python load_csv_data.py
        python predict_all_customers.py
    fi
fi

echo "🎉 Starting uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
