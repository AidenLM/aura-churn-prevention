"""Seed database with sample customer data"""
import random
from datetime import datetime, timedelta
from app.db.base import SessionLocal, engine
from app.db.models import Base, Customer, PredictionRecord, Campaign
from app.services.churn_predictor import ChurnPredictor
from app.schemas.customer import CustomerFeatures

# Create tables
Base.metadata.create_all(bind=engine)

# Sample Turkish names
FIRST_NAMES = [
    "Ahmet", "Mehmet", "Mustafa", "Ali", "Hüseyin", "Hasan", "İbrahim", "Yusuf",
    "Ayşe", "Fatma", "Emine", "Hatice", "Zeynep", "Elif", "Meryem", "Şeyma"
]

LAST_NAMES = [
    "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Yıldırım", "Öztürk",
    "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara"
]

PLAN_TYPES = ["Standart", "Premium", "Premium Unlimited", "Ekonomik", "Aile Paketi"]
CONTRACT_TYPES = ["Monthly", "Annual"]

def generate_phone():
    """Generate Turkish phone number"""
    return f"+90 5{random.randint(10, 59)} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}"

def generate_email(name, surname):
    """Generate email address"""
    domains = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com"]
    return f"{name.lower()}.{surname.lower()}@{random.choice(domains)}"

def create_sample_customers(db, count=250):
    """Create sample customers with realistic hybrid model data"""
    print(f"Creating {count} sample customers with hybrid model features...")
    
    predictor = ChurnPredictor()
    customers_created = 0
    
    for i in range(count):
        # Generate customer data
        name = random.choice(FIRST_NAMES)
        surname = random.choice(LAST_NAMES)
        full_name = f"{name} {surname}"
        
        # Age distribution (18-75)
        age = random.choices(
            [random.randint(18, 30), random.randint(30, 50), random.randint(50, 75)],
            weights=[0.35, 0.45, 0.20]
        )[0]
        
        # Gender (0=Female, 1=Male)
        gender = random.randint(0, 1)
        
        # Realistic feature distributions
        tenure_months = random.choices(
            [random.randint(1, 6), random.randint(6, 24), random.randint(24, 72)],
            weights=[0.3, 0.5, 0.2]
        )[0]
        
        plan_type = random.choice(PLAN_TYPES)
        
        if plan_type == "Ekonomik":
            monthly_charge = round(random.uniform(99.99, 149.99), 2)
        elif plan_type == "Standart":
            monthly_charge = round(random.uniform(149.99, 199.99), 2)
        elif plan_type == "Premium":
            monthly_charge = round(random.uniform(199.99, 299.99), 2)
        elif plan_type == "Premium Unlimited":
            monthly_charge = round(random.uniform(299.99, 399.99), 2)
        else:  # Aile Paketi
            monthly_charge = round(random.uniform(249.99, 349.99), 2)
        
        data_usage_gb = round(random.uniform(0.5, 50.0), 1)
        voice_minutes = random.randint(0, 1500)
        sms_count = random.randint(0, 500)
        
        # Risk indicators - more varied distribution
        risk_profile = random.random()
        if risk_profile < 0.20:  # 20% high-risk profile
            complaint_count = random.randint(3, 10)
            call_failures = random.randint(10, 30)  # NEW
            support_calls_count = random.randint(5, 15)
            payment_delays = random.randint(2, 5)
        elif risk_profile < 0.50:  # 30% medium-risk profile
            complaint_count = random.randint(1, 3)
            call_failures = random.randint(3, 10)  # NEW
            support_calls_count = random.randint(2, 5)
            payment_delays = random.randint(0, 2)
        else:  # 50% low-risk profile
            complaint_count = random.randint(0, 1)
            call_failures = random.randint(0, 3)  # NEW
            support_calls_count = random.randint(0, 2)
            payment_delays = 0
        
        contract_type = random.choices(
            CONTRACT_TYPES,
            weights=[0.7, 0.3]  # 70% monthly, 30% annual
        )[0]
        
        customer = Customer(
            customer_id=f"C{10000 + i}",
            name=full_name,
            email=generate_email(name, surname),
            phone=generate_phone(),
            plan_type=plan_type,
            tenure_months=tenure_months,  # RENAMED
            monthly_charge=monthly_charge,
            age=age,  # NEW
            gender=gender,  # NEW
            data_usage_gb=data_usage_gb,
            voice_minutes=voice_minutes,
            sms_count=sms_count,
            complaint_count=complaint_count,
            call_failures=call_failures,  # NEW
            support_calls_count=support_calls_count,
            payment_delays=payment_delays,
            contract_type=contract_type
        )
        
        db.add(customer)
        customers_created += 1
        
        # Generate prediction for this customer
        features = CustomerFeatures(
            tenure=tenure_months,
            monthly_charge=float(monthly_charge),
            age=age,  # NEW
            gender=gender,  # NEW
            data_usage_gb=float(data_usage_gb),
            voice_minutes=voice_minutes,
            sms_count=sms_count,
            complaint_count=complaint_count,
            call_failures=call_failures,  # NEW
            support_calls_count=support_calls_count,
            payment_delays=payment_delays,
            plan_type=plan_type,
            contract_type=contract_type
        )
        
        prediction = predictor.predict(features)
        
        # Create prediction record
        pred_record = PredictionRecord(
            customer_id=customer.customer_id,
            risk_score=prediction.risk_score,
            risk_level=prediction.risk_level,
            shap_values={},  # Empty for now
            timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        )
        
        db.add(pred_record)
    
    db.commit()
    print(f"✅ Created {customers_created} customers with hybrid model features")

def create_campaigns(db):
    """Create sample campaigns"""
    print("Creating campaign catalog...")
    
    campaigns = [
        Campaign(
            campaign_id="CAMP001",
            name_tr="%30 İndirim Kampanyası",
            discount_percentage=30,
            duration_months=6,
            cost_per_customer=539.97,
            target_segments=["high_risk", "price_sensitive"],
            min_tenure=0,
            max_monthly_charge=400.0,
            is_active=True
        ),
        Campaign(
            campaign_id="CAMP002",
            name_tr="%20 İndirim + Ekstra 10GB",
            discount_percentage=20,
            duration_months=3,
            cost_per_customer=359.98,
            target_segments=["high_risk", "data_user"],
            min_tenure=0,
            max_monthly_charge=300.0,
            is_active=True
        ),
        Campaign(
            campaign_id="CAMP003",
            name_tr="Sadakat Bonusu - %15 İndirim",
            discount_percentage=15,
            duration_months=12,
            cost_per_customer=539.96,
            target_segments=["medium_risk", "loyal"],
            min_tenure=12,
            max_monthly_charge=None,
            is_active=True
        ),
        Campaign(
            campaign_id="CAMP004",
            name_tr="Yeni Müşteri Özel - %25 İndirim",
            discount_percentage=25,
            duration_months=6,
            cost_per_customer=449.97,
            target_segments=["high_risk", "new_customer"],
            min_tenure=0,
            max_monthly_charge=350.0,
            is_active=True
        ),
        Campaign(
            campaign_id="CAMP005",
            name_tr="Premium Paket İndirimi - %10",
            discount_percentage=10,
            duration_months=6,
            cost_per_customer=539.94,
            target_segments=["medium_risk", "premium"],
            min_tenure=6,
            max_monthly_charge=None,
            is_active=True
        ),
    ]
    
    for campaign in campaigns:
        db.add(campaign)
    
    db.commit()
    print(f"✅ Created {len(campaigns)} campaigns")

def main():
    """Main seeding function"""
    print("=" * 60)
    print("AURA Database Seeding")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        from app.db.models import Customer
        existing_count = db.query(Customer).count()
        
        if existing_count > 0:
            print(f"\n⚠️  Database already has {existing_count} customers")
            response = input("Do you want to clear and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("Seeding cancelled")
                return
            
            # Clear existing data
            print("\nClearing existing data...")
            db.query(PredictionRecord).delete()
            db.query(Customer).delete()
            db.query(Campaign).delete()
            db.commit()
            print("✅ Cleared existing data")
        
        # Create sample data
        print()
        create_sample_customers(db, count=250)
        print()
        create_campaigns(db)
        
        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        
        # Show summary
        customer_count = db.query(Customer).count()
        prediction_count = db.query(PredictionRecord).count()
        campaign_count = db.query(Campaign).count()
        
        print(f"\nDatabase Summary:")
        print(f"  Customers: {customer_count}")
        print(f"  Predictions: {prediction_count}")
        print(f"  Campaigns: {campaign_count}")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
