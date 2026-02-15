from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    """Base customer schema - TrustedModel features"""
    customer_id: str = Field(..., description="Unique customer identifier")
    
    # Demographic Features
    gender: str = Field(..., description="Male or Female")
    senior_citizen: int = Field(..., ge=0, le=1, description="0=No, 1=Yes")
    partner: str = Field(..., description="Yes or No")
    dependents: str = Field(..., description="Yes or No")
    
    # Account Information
    tenure: int = Field(..., ge=0, description="Months as customer")
    contract: str = Field(..., description="Month-to-month, One year, Two year")
    paperless_billing: str = Field(..., description="Yes or No")
    payment_method: str = Field(..., description="Payment method type")
    monthly_charges: float = Field(..., ge=0, description="Monthly charges in currency")
    total_charges: float = Field(..., ge=0, description="Total charges to date")
    
    # Phone Services
    phone_service: str = Field(..., description="Yes or No")
    multiple_lines: str = Field(..., description="Yes, No, or No phone service")
    
    # Internet Services
    internet_service: str = Field(..., description="DSL, Fiber optic, or No")
    online_security: str = Field(..., description="Yes, No, or No internet service")
    online_backup: str = Field(..., description="Yes, No, or No internet service")
    device_protection: str = Field(..., description="Yes, No, or No internet service")
    tech_support: str = Field(..., description="Yes, No, or No internet service")
    streaming_tv: str = Field(..., description="Yes, No, or No internet service")
    streaming_movies: str = Field(..., description="Yes, No, or No internet service")
    
    # Optional - actual churn status if known
    churn: Optional[str] = Field(None, description="Yes or No - actual churn status")


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating customer information"""
    gender: Optional[str] = None
    senior_citizen: Optional[int] = None
    partner: Optional[str] = None
    dependents: Optional[str] = None
    tenure: Optional[int] = None
    contract: Optional[str] = None
    paperless_billing: Optional[str] = None
    payment_method: Optional[str] = None
    monthly_charges: Optional[float] = None
    total_charges: Optional[float] = None
    phone_service: Optional[str] = None
    multiple_lines: Optional[str] = None
    internet_service: Optional[str] = None
    online_security: Optional[str] = None
    online_backup: Optional[str] = None
    device_protection: Optional[str] = None
    tech_support: Optional[str] = None
    streaming_tv: Optional[str] = None
    streaming_movies: Optional[str] = None
    churn: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response with timestamps"""
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChurnPredictionRequest(BaseModel):
    """Schema for churn prediction request"""
    customer_id: str


class ChurnPredictionResponse(BaseModel):
    """Schema for churn prediction response"""
    customer_id: str
    churn_probability: float = Field(..., ge=0, le=1, description="Probability of churn (0-1)")
    predicted_churn: str = Field(..., description="Yes or No")
    risk_level: str = Field(..., description="Low, Medium, or High")
    model_name: str = Field(..., description="Model used for prediction")
    
    # Customer summary for display
    tenure: int
    monthly_charges: float
    contract: str
    internet_service: str


class BulkPredictionRequest(BaseModel):
    """Schema for bulk prediction request"""
    customer_ids: list[str] = Field(..., description="List of customer IDs")


class BulkPredictionResponse(BaseModel):
    """Schema for bulk prediction response"""
    predictions: list[ChurnPredictionResponse]
    total_customers: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
