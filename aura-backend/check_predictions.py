"""
Check prediction status for all customers
"""
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('aura_dev.db')
cursor = conn.cursor()

# Get total customers
cursor.execute("SELECT COUNT(*) FROM customers")
total_customers = cursor.fetchone()[0]

# Get customers with predictions
cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM predictions")
customers_with_predictions = cursor.fetchone()[0]

# Get total predictions
cursor.execute("SELECT COUNT(*) FROM predictions")
total_predictions = cursor.fetchone()[0]

# Get risk distribution (all predictions)
cursor.execute("""
    SELECT risk_level, COUNT(*) 
    FROM predictions 
    GROUP BY risk_level
""")
risk_distribution = dict(cursor.fetchall())

# Get latest prediction timestamp
cursor.execute("SELECT MAX(timestamp) FROM predictions")
latest_date = cursor.fetchone()[0]

print("=" * 60)
print("PREDICTION STATUS CHECK")
print("=" * 60)
print(f"\nTotal Customers: {total_customers:,}")
print(f"Customers with Predictions: {customers_with_predictions:,}")
print(f"Total Predictions: {total_predictions:,}")
print(f"\nPrediction Coverage: {(customers_with_predictions/total_customers*100):.2f}%")

if customers_with_predictions == total_customers:
    print("\n✅ ALL CUSTOMERS HAVE PREDICTIONS!")
else:
    missing = total_customers - customers_with_predictions
    print(f"\n⚠️  {missing:,} customers are missing predictions")

print(f"\n📊 Risk Distribution (Latest Predictions):")
for level in ['Low', 'Medium', 'High']:
    count = risk_distribution.get(level, 0)
    pct = (count / customers_with_predictions * 100) if customers_with_predictions > 0 else 0
    print(f"   {level}: {count:,} ({pct:.1f}%)")

print(f"\n📅 Latest Prediction Date: {latest_date}")

# Show sample customers without predictions if any
if customers_with_predictions < total_customers:
    cursor.execute("""
        SELECT customer_id 
        FROM customers 
        WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM predictions)
        LIMIT 5
    """)
    missing_customers = cursor.fetchall()
    
    if missing_customers:
        print(f"\nSample customers without predictions:")
        for (customer_id,) in missing_customers:
            print(f"   - {customer_id}")

print("\n" + "=" * 60)

conn.close()
