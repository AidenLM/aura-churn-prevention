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

# CORS middleware - Allow production and development origins
allowed_origins = [
    settings.FRONTEND_URL,
    "https://nativestruct.com",
    "https://www.nativestruct.com",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
        
        # Create 50 sample customers using TrustedModel schema
        GENDERS = ["Male", "Female"]
        YES_NO = ["Yes", "No"]
        CONTRACTS = ["Month-to-month", "One year", "Two year"]
        PAYMENT_METHODS = ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        INTERNET_SERVICES = ["DSL", "Fiber optic", "No"]
        INTERNET_OPTIONS = ["Yes", "No", "No internet service"]
        PHONE_OPTIONS = ["Yes", "No", "No phone service"]
        
        for i in range(50):
            tenure = random.randint(1, 72)
            monthly_charges = round(random.uniform(20, 120), 2)
            total_charges = round(monthly_charges * tenure, 2)
            risk_score = random.uniform(0, 1)
            
            customer = Customer(
                customer_id=f"C{10000 + i}",
                gender=random.choice(GENDERS),
                senior_citizen=random.randint(0, 1),
                partner=random.choice(YES_NO),
                dependents=random.choice(YES_NO),
                tenure=tenure,
                contract=random.choice(CONTRACTS),
                paperless_billing=random.choice(YES_NO),
                payment_method=random.choice(PAYMENT_METHODS),
                monthly_charges=monthly_charges,
                total_charges=total_charges,
                phone_service=random.choice(YES_NO),
                multiple_lines=random.choice(PHONE_OPTIONS),
                internet_service=random.choice(INTERNET_SERVICES),
                online_security=random.choice(INTERNET_OPTIONS),
                online_backup=random.choice(INTERNET_OPTIONS),
                device_protection=random.choice(INTERNET_OPTIONS),
                tech_support=random.choice(INTERNET_OPTIONS),
                streaming_tv=random.choice(INTERNET_OPTIONS),
                streaming_movies=random.choice(INTERNET_OPTIONS),
                churn="No"
            )
            db.add(customer)
            
            # Create prediction record
            if risk_score >= 0.7:
                risk_level = "high"
            elif risk_score >= 0.4:
                risk_level = "medium"
            else:
                risk_level = "low"
                
            pred_record = PredictionRecord(
                customer_id=customer.customer_id,
                churn_probability=risk_score,
                risk_score=risk_score,
                risk_level=risk_level,
                predicted_churn="Yes" if risk_score >= 0.5 else "No",
                model_name="Voting Classifier",
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
