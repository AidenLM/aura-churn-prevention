from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, DECIMAL
from sqlalchemy.sql import func
from app.db.base import Base

class Customer(Base):
    """Customer table - TrustedModel Telco Customer Churn dataset"""
    __tablename__ = "customers"
    
    # Primary Key
    customer_id = Column(String(50), primary_key=True, index=True)
    
    # Demographic Features (4)
    gender = Column(String(10))  # Male, Female
    senior_citizen = Column(Integer)  # 0 or 1
    partner = Column(String(10))  # Yes, No
    dependents = Column(String(10))  # Yes, No
    
    # Account Information (5)
    tenure = Column(Integer)  # months as customer
    contract = Column(String(50))  # Month-to-month, One year, Two year
    paperless_billing = Column(String(10))  # Yes, No
    payment_method = Column(String(50))  # Electronic check, Mailed check, Bank transfer, Credit card
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    
    # Phone Services (2)
    phone_service = Column(String(10))  # Yes, No
    multiple_lines = Column(String(50))  # Yes, No, No phone service
    
    # Internet Services (8)
    internet_service = Column(String(50))  # DSL, Fiber optic, No
    online_security = Column(String(50))  # Yes, No, No internet service
    online_backup = Column(String(50))  # Yes, No, No internet service
    device_protection = Column(String(50))  # Yes, No, No internet service
    tech_support = Column(String(50))  # Yes, No, No internet service
    streaming_tv = Column(String(50))  # Yes, No, No internet service
    streaming_movies = Column(String(50))  # Yes, No, No internet service
    
    # Target (for display/tracking)
    churn = Column(String(10))  # Yes, No (actual churn status if known)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PredictionRecord(Base):
    """Predictions audit trail - stores all churn predictions"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    churn_probability = Column(Float, nullable=False)  # 0.0 to 1.0 (same as risk_score)
    risk_score = Column(Float, nullable=False)  # Alias for churn_probability
    risk_level = Column(String(20), nullable=False)  # Low, Medium, High
    predicted_churn = Column(String(10), nullable=False)  # Yes, No
    model_name = Column(String(100))  # Voting Classifier
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_id = Column(String(50))


class Campaign(Base):
    """Campaigns catalog - available retention offers"""
    __tablename__ = "campaigns"
    
    campaign_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    discount_percentage = Column(Integer)
    duration_months = Column(Integer)
    cost_per_customer = Column(Float)
    target_segments = Column(JSON)  # List of target customer segments
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    """Users table - system users for authentication"""
    __tablename__ = "users"
    
    user_id = Column(String(50), primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50))  # admin, manager, analyst
    created_at = Column(DateTime(timezone=True), server_default=func.now())
