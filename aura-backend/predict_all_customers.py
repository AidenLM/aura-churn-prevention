"""
Predict churn risk for all customers in database
"""
import sys
import os

# Set working directory to aura-backend
os.chdir('aura-backend')
sys.path.insert(0, '.')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.db.models import Customer
from app.services.churn_predictor import ChurnPredictor
from app.repositories.customer_repository import CustomerRepository

def predict_all_customers():
    """Run predictions for all customers"""
    db = SessionLocal()
    predictor = ChurnPredictor()
    repo = CustomerRepository(db)
    
    try:
        # Get all customers
        customers = db.query(Customer).all()
        total = len(customers)
        
        print(f"🔄 Starting predictions for {total} customers...")
        
        success_count = 0
        error_count = 0
        
        for i, customer in enumerate(customers, 1):
            try:
                # Prepare customer data
                customer_data = {
                    "customer_id": customer.customer_id,
                    "gender": customer.gender,
                    "senior_citizen": customer.senior_citizen,
                    "partner": customer.partner,
                    "dependents": customer.dependents,
                    "tenure": customer.tenure,
                    "contract": customer.contract,
                    "paperless_billing": customer.paperless_billing,
                    "payment_method": customer.payment_method,
                    "monthly_charges": float(customer.monthly_charges),
                    "total_charges": float(customer.total_charges),
                    "phone_service": customer.phone_service,
                    "multiple_lines": customer.multiple_lines,
                    "internet_service": customer.internet_service,
                    "online_security": customer.online_security,
                    "online_backup": customer.online_backup,
                    "device_protection": customer.device_protection,
                    "tech_support": customer.tech_support,
                    "streaming_tv": customer.streaming_tv,
                    "streaming_movies": customer.streaming_movies
                }
                
                # Get prediction
                prediction = predictor.predict(customer_data)
                
                # Save to database
                repo.save_prediction(
                    customer_id=customer.customer_id,
                    risk_score=prediction["churn_probability"],
                    risk_level=prediction["risk_level"]
                )
                
                success_count += 1
                
                # Progress update every 500 customers
                if i % 500 == 0:
                    print(f"   Progress: {i}/{total} ({(i/total)*100:.1f}%)")
                    
            except Exception as e:
                error_count += 1
                print(f"   ❌ Error for customer {customer.customer_id}: {e}")
        
        print(f"\n✅ Predictions complete!")
        print(f"   Success: {success_count}")
        print(f"   Errors: {error_count}")
        print(f"   Total: {total}")
        
        # Show statistics
        stats = repo.get_summary_stats(use_cache=False)
        print(f"\n📊 Risk Distribution:")
        print(f"   Low: {stats.risk_distribution['low']}")
        print(f"   Medium: {stats.risk_distribution['medium']}")
        print(f"   High: {stats.risk_distribution['high']}")
        print(f"   Average Risk: {stats.average_risk:.2%}")
        
    finally:
        db.close()

if __name__ == "__main__":
    predict_all_customers()
