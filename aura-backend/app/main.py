from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import dashboard, customers, prediction, simulation
from app.db.base import Base, engine
import os

app = FastAPI(
    title="AURA API",
    description="AI-powered Customer Churn Prevention System",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Seed database if empty
    from sqlalchemy.orm import Session
    from app.db.models import Customer, PredictionRecord, Campaign
    from app.services.churn_predictor import ChurnPredictor
    from app.schemas.customer import CustomerFeatures
    import random
    from datetime import datetime, timedelta
    
    db = Session(bind=engine)
    try:
        count = db.query(Customer).count()
        if count == 0:
            print("Database is empty, seeding data...")
            
            # Create sample customers
            predictor = ChurnPredictor()
            FIRST_NAMES = ["Ahmet", "Mehmet", "Mustafa", "Ali", "Ayşe", "Fatma", "Zeynep"]
            LAST_NAMES = ["Yılmaz", "Kaya", "Demir", "Şahin", "Öztürk"]
            PLAN_TYPES = ["Standart", "Premium", "Ekonomik"]
            
            for i in range(50):  # Create 50 customers
                name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                tenure = random.randint(1, 72)
                monthly_charge = round(random.uniform(100, 400), 2)
                
                customer = Customer(
                    customer_id=f"C{10000 + i}",
                    name=name,
                    email=f"customer{i}@example.com",
                    phone=f"+90 5{random.randint(10, 59)} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}",
                    plan_type=random.choice(PLAN_TYPES),
                    tenure_months=tenure,
                    monthly_charge=monthly_charge,
                    age=random.randint(18, 75),
                    gender=random.randint(0, 1),
                    data_usage_gb=round(random.uniform(1, 50), 1),
                    voice_minutes=random.randint(0, 1500),
                    sms_count=random.randint(0, 500),
                    complaint_count=random.randint(0, 5),
                    call_failures=random.randint(0, 20),
                    support_calls_count=random.randint(0, 10),
                    payment_delays=random.randint(0, 3),
                    contract_type=random.choice(["Monthly", "Annual"])
                )
                db.add(customer)
                
                # Create prediction
                features = CustomerFeatures(
                    tenure=tenure,
                    monthly_charge=float(monthly_charge),
                    age=customer.age,
                    gender=customer.gender,
                    data_usage_gb=float(customer.data_usage_gb),
                    voice_minutes=customer.voice_minutes,
                    sms_count=customer.sms_count,
                    complaint_count=customer.complaint_count,
                    call_failures=customer.call_failures,
                    support_calls_count=customer.support_calls_count,
                    payment_delays=customer.payment_delays,
                    plan_type=customer.plan_type,
                    contract_type=customer.contract_type
                )
                prediction = predictor.predict(features)
                
                pred_record = PredictionRecord(
                    customer_id=customer.customer_id,
                    risk_score=prediction.risk_score,
                    risk_level=prediction.risk_level,
                    shap_values={},
                    timestamp=datetime.utcnow()
                )
                db.add(pred_record)
            
            db.commit()
            print("✅ Database seeded with 50 customers")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router)
app.include_router(customers.router)
app.include_router(prediction.router)
app.include_router(simulation.router)

@app.get("/")
async def root():
    return {
        "message": "AURA API - Müşteri Kaybı Önleme Sistemi",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
