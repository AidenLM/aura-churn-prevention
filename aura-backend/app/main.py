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
    print("✅ Database tables created")

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

@app.post("/seed-database")
async def seed_database():
    """Manually seed the database with sample data"""
    from sqlalchemy.orm import Session
    from app.db.models import Customer, PredictionRecord
    import random
    from datetime import datetime
    
    db = Session(bind=engine)
    try:
        # Check if already seeded
        count = db.query(Customer).count()
        if count > 0:
            return {"message": f"Database already has {count} customers", "seeded": False}
        
        # Create 50 sample customers (simplified - no predictions for now)
        FIRST_NAMES = ["Ahmet", "Mehmet", "Mustafa", "Ali", "Ayşe", "Fatma", "Zeynep"]
        LAST_NAMES = ["Yılmaz", "Kaya", "Demir", "Şahin", "Öztürk"]
        PLAN_TYPES = ["Standart", "Premium", "Ekonomik"]
        
        for i in range(50):
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            tenure = random.randint(1, 72)
            monthly_charge = round(random.uniform(100, 400), 2)
            risk_score = random.uniform(0, 1)
            
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
            
            # Create simple prediction record
            if risk_score >= 0.7:
                risk_level = "high"
            elif risk_score >= 0.4:
                risk_level = "medium"
            else:
                risk_level = "low"
                
            pred_record = PredictionRecord(
                customer_id=customer.customer_id,
                risk_score=risk_score,
                risk_level=risk_level,
                shap_values={},
                timestamp=datetime.utcnow()
            )
            db.add(pred_record)
        
        db.commit()
        return {"message": "Database seeded with 50 customers", "seeded": True, "count": 50}
    except Exception as e:
        db.rollback()
        return {"error": str(e), "seeded": False}
    finally:
        db.close()
