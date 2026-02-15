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

@app.post("/predict-all-customers")
async def predict_all_customers():
    """Run ML predictions for all customers in database"""
    from sqlalchemy.orm import Session
    from app.db.models import Customer
    from app.services.churn_predictor import ChurnPredictor
    from app.repositories.customer_repository import CustomerRepository
    
    db = Session(bind=engine)
    try:
        predictor = ChurnPredictor()
        repo = CustomerRepository(db)
        
        # Get all customers
        customers = db.query(Customer).all()
        total = len(customers)
        
        if total == 0:
            return {"message": "No customers in database", "predicted": 0}
        
        success_count = 0
        error_count = 0
        
        for customer in customers:
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
                
                # Get ML prediction
                prediction = predictor.predict(customer_data)
                
                # Save to database (overwrites existing)
                repo.save_prediction(
                    customer_id=customer.customer_id,
                    risk_score=prediction["churn_probability"],
                    risk_level=prediction["risk_level"]
                )
                
                success_count += 1
                    
            except Exception as e:
                error_count += 1
                print(f"Error for customer {customer.customer_id}: {e}")
        
        return {
            "message": "Predictions complete",
            "total": total,
            "success": success_count,
            "errors": error_count
        }
        
    except Exception as e:
        db.rollback()
        return {"error": str(e), "predicted": 0}
    finally:
        db.close()

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
