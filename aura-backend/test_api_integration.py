"""
Test API Integration with TrustedModel
"""
import sys
import os

# Set working directory to aura-backend
os.chdir('aura-backend')
sys.path.insert(0, '.')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from app.services.churn_predictor import ChurnPredictor
from app.db.base import SessionLocal
from app.repositories.customer_repository import CustomerRepository

def test_predictor():
    """Test ChurnPredictor service"""
    print("\n=== Testing ChurnPredictor ===")
    
    predictor = ChurnPredictor()
    
    # Test customer data
    customer = {
        'customer_id': 'TEST-001',
        'gender': 'Male',
        'senior_citizen': 0,
        'partner': 'Yes',
        'dependents': 'No',
        'tenure': 12,
        'phone_service': 'Yes',
        'multiple_lines': 'No',
        'internet_service': 'Fiber optic',
        'online_security': 'No',
        'online_backup': 'No',
        'device_protection': 'No',
        'tech_support': 'No',
        'streaming_tv': 'Yes',
        'streaming_movies': 'Yes',
        'contract': 'Month-to-month',
        'paperless_billing': 'Yes',
        'payment_method': 'Electronic check',
        'monthly_charges': 85.0,
        'total_charges': 1020.0
    }
    
    result = predictor.predict(customer)
    print(f"✅ Prediction successful")
    print(f"   Customer ID: {result['customer_id']}")
    print(f"   Churn Probability: {result['churn_probability']:.2%}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Predicted Churn: {result['predicted_churn']}")
    
    return True

def test_database():
    """Test database connection and customer retrieval"""
    print("\n=== Testing Database ===")
    
    db = SessionLocal()
    try:
        repo = CustomerRepository(db)
        
        # Get total customers
        total = repo.count_customers()
        print(f"✅ Total customers in database: {total}")
        
        # Get random customer
        customer = repo.get_random_customer()
        if customer:
            print(f"✅ Random customer retrieved: {customer.customer_id}")
            print(f"   Gender: {customer.gender}")
            print(f"   Tenure: {customer.tenure} months")
            print(f"   Contract: {customer.contract}")
            print(f"   Monthly Charges: ${customer.monthly_charges:.2f}")
            
            # Test prediction on real customer
            predictor = ChurnPredictor()
            customer_data = {
                'customer_id': customer.customer_id,
                'gender': customer.gender,
                'senior_citizen': customer.senior_citizen,
                'partner': customer.partner,
                'dependents': customer.dependents,
                'tenure': customer.tenure,
                'phone_service': customer.phone_service,
                'multiple_lines': customer.multiple_lines,
                'internet_service': customer.internet_service,
                'online_security': customer.online_security,
                'online_backup': customer.online_backup,
                'device_protection': customer.device_protection,
                'tech_support': customer.tech_support,
                'streaming_tv': customer.streaming_tv,
                'streaming_movies': customer.streaming_movies,
                'contract': customer.contract,
                'paperless_billing': customer.paperless_billing,
                'payment_method': customer.payment_method,
                'monthly_charges': float(customer.monthly_charges),
                'total_charges': float(customer.total_charges)
            }
            
            prediction = predictor.predict(customer_data)
            print(f"✅ Prediction for real customer:")
            print(f"   Churn Probability: {prediction['churn_probability']:.2%}")
            print(f"   Risk Level: {prediction['risk_level']}")
            
            # Save prediction
            repo.save_prediction(
                customer_id=customer.customer_id,
                risk_score=prediction['churn_probability'],
                risk_level=prediction['risk_level']
            )
            print(f"✅ Prediction saved to database")
        else:
            print("❌ No customers found in database")
            return False
        
        # Get summary stats
        stats = repo.get_summary_stats(use_cache=False)
        print(f"\n✅ Dashboard Statistics:")
        print(f"   Total Customers: {stats.total_customers}")
        print(f"   High Risk Count: {stats.high_risk_count}")
        print(f"   Average Risk: {stats.average_risk:.2%}")
        print(f"   Risk Distribution: {stats.risk_distribution}")
        
        return True
        
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("AURA Backend Integration Test - TrustedModel")
    print("=" * 60)
    
    try:
        # Test predictor
        if not test_predictor():
            print("\n❌ Predictor test failed")
            sys.exit(1)
        
        # Test database
        if not test_database():
            print("\n❌ Database test failed")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
