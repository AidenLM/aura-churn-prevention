"""
Load TrustedModel Telco Customer Churn dataset into database
"""
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.models import Customer
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aura_dev.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Drop all tables and recreate
print("🗑️  Dropping existing tables...")
Base.metadata.drop_all(bind=engine)

print("🔨 Creating new tables...")
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

print("\n📊 Loading TrustedModel dataset...")
df = pd.read_csv('TrustedModel/WA_Fn-UseC_-Telco-Customer-Churn.csv')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Clean TotalCharges (has some spaces)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

print(f"\n💾 Inserting {len(df)} customers into database...")

# Insert customers
batch_size = 100
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    
    for _, row in batch.iterrows():
        customer = Customer(
            customer_id=row['customerID'],
            gender=row['gender'],
            senior_citizen=int(row['SeniorCitizen']),
            partner=row['Partner'],
            dependents=row['Dependents'],
            tenure=int(row['tenure']),
            phone_service=row['PhoneService'],
            multiple_lines=row['MultipleLines'],
            internet_service=row['InternetService'],
            online_security=row['OnlineSecurity'],
            online_backup=row['OnlineBackup'],
            device_protection=row['DeviceProtection'],
            tech_support=row['TechSupport'],
            streaming_tv=row['StreamingTV'],
            streaming_movies=row['StreamingMovies'],
            contract=row['Contract'],
            paperless_billing=row['PaperlessBilling'],
            payment_method=row['PaymentMethod'],
            monthly_charges=float(row['MonthlyCharges']),
            total_charges=float(row['TotalCharges']),
            churn=row['Churn']
        )
        db.add(customer)
    
    db.commit()
    print(f"  ✅ Inserted {min(i+batch_size, len(df))}/{len(df)} customers")

print("\n✅ Data loading completed!")

# Statistics
print("\n📈 Database Statistics:")
total_customers = db.query(Customer).count()
churned_customers = db.query(Customer).filter(Customer.churn == 'Yes').count()
churn_rate = (churned_customers / total_customers) * 100

print(f"Total customers: {total_customers}")
print(f"Churned customers: {churned_customers}")
print(f"Churn rate: {churn_rate:.2f}%")

# Sample customers
print("\n👥 Sample customers:")
sample_customers = db.query(Customer).limit(5).all()
for customer in sample_customers:
    print(f"  - {customer.customer_id}: {customer.gender}, Tenure: {customer.tenure} months, "
          f"Contract: {customer.contract}, Churn: {customer.churn}")

db.close()
print("\n🎉 Done!")
