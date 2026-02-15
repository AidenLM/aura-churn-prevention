#!/bin/bash

# Hybrid Model Deployment Script
# This script deploys the trained hybrid model to AURA backend

echo "=========================================="
echo "AURA Hybrid Model Deployment"
echo "=========================================="
echo ""

# Check if model files exist
echo "📦 Checking model files..."
if [ ! -f "models/churn_model.pkl" ]; then
    echo "❌ Error: models/churn_model.pkl not found"
    echo "   Please copy model files from Google Colab to aura-backend/models/"
    exit 1
fi

if [ ! -f "models/feature_names.pkl" ]; then
    echo "❌ Error: models/feature_names.pkl not found"
    exit 1
fi

echo "✅ Model files found"
echo ""

# Verify feature names
echo "🔍 Verifying model features..."
FEATURES=$(python3 -c "import joblib; print(joblib.load('models/feature_names.pkl'))" 2>/dev/null)
if [[ $FEATURES == *"tenure_months"* ]] && [[ $FEATURES == *"call_failures"* ]]; then
    echo "✅ Hybrid model features verified"
    echo "   Features: $FEATURES"
else
    echo "❌ Error: Wrong model! Expected hybrid model features"
    echo "   Got: $FEATURES"
    exit 1
fi
echo ""

# Ask user about database
echo "🗄️  Database migration options:"
echo "   1) Migrate existing database (add new columns)"
echo "   2) Fresh database (delete and reseed)"
echo "   3) Skip database migration"
echo ""
read -p "Choose option (1/2/3): " DB_OPTION

if [ "$DB_OPTION" == "1" ]; then
    echo ""
    echo "📝 Migrating existing database..."
    python3 migrate_to_hybrid.py
    if [ $? -ne 0 ]; then
        echo "❌ Migration failed"
        exit 1
    fi
elif [ "$DB_OPTION" == "2" ]; then
    echo ""
    echo "⚠️  This will DELETE all existing data!"
    read -p "Are you sure? (yes/no): " CONFIRM
    if [ "$CONFIRM" == "yes" ]; then
        echo "🗑️  Deleting old database..."
        rm -f aura_dev.db
        echo "📝 Creating fresh database..."
        python3 seed_database.py
        if [ $? -ne 0 ]; then
            echo "❌ Database seeding failed"
            exit 1
        fi
    else
        echo "❌ Cancelled"
        exit 1
    fi
elif [ "$DB_OPTION" == "3" ]; then
    echo "⏭️  Skipping database migration"
else
    echo "❌ Invalid option"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart backend server: ./start_server.sh"
echo "2. Check logs for model loading confirmation"
echo "3. Test API: curl http://localhost:8000/api/customers"
echo "4. Open frontend: http://localhost:3000"
echo ""
echo "For troubleshooting, see: HYBRID_MODEL_DEPLOYMENT.md"
