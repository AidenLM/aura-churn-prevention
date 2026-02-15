"""Load TrustedModel CSV data into database"""
import pandas as pd
from app.db.base import SessionLocal
from app.db.models import Customer, PredictionRecord, Base, engine
from datetime import datetime
import random

# Create tables
Base.metadata.create_all(bind=engine)

# Load CSV
df = pd.read_csv("TrustedModel/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Take first 100 customers
df = df.head(100)

db = SessionLocal()

try:
    for idx, row in df.iterrows():
        # Handle TotalCharges (can be empty string)
        total_charges = float(row['TotalCharges']) if row['TotalCharges'] != ' ' else 0.0
        
        customer = Customer(
            customer_id=row['customerID'],
            gender=row['gender'],
            senior_citizen=int(row['SeniorCitizen']),
            partner=row['Partner'],
            dependents=row['Dependents'],
            tenure=int(row['tenure']),
            contract=row['Contract'],
            paperless_billing=row['PaperlessBilling'],
            payment_method=row['PaymentMethod'],
            monthly_charges=float(row['MonthlyCharges']),
            total_charges=total_charges,
            phone_service=row['PhoneService'],
            multiple_lines=row['MultipleLines'],
            internet_service=row['InternetService'],
            online_security=row['OnlineSecurity'],
            online_backup=row['OnlineBackup'],
            device_protection=row['DeviceProtection'],
            tech_support=row['TechSupport'],
            streaming_tv=row['StreamingTV'],
            streaming_movies=row['StreamingMovies'],
            churn=row['Churn']
        )
        db.add(customer)
        
        # Create prediction record
        risk_score = random.uniform(0, 1)
        if risk_score >= 0.7:
            risk_level = "high"
        elif risk_score >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
            
        pred_record = PredictionRecord(
            customer_id=row['customerID'],
            churn_probability=risk_score,
            risk_score=risk_score,
            risk_level=risk_level,
            predicted_churn="Yes" if risk_score >= 0.5 else "No",
            model_name="Voting Classifier",
            timestamp=datetime.utcnow()
        )
        db.add(pred_record)
    
    db.commit()
    print(f"✅ Loaded {len(df)} customers from CSV")
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
