"""Prediction API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.db.base import get_db
from app.services.churn_predictor import ChurnPredictor

router = APIRouter(prefix="/api/predict", tags=["prediction"])

# Initialize services
predictor = ChurnPredictor()


class ShapFeature(BaseModel):
    """SHAP feature importance"""
    feature_name: str
    importance: float
    direction: str
    display_name_tr: str


class PredictionRequest(BaseModel):
    """Risk prediction request - TrustedModel features"""
    # Demographic (4)
    gender: str = Field(..., description="Gender (Male/Female)")
    senior_citizen: int = Field(..., ge=0, le=1, description="Senior citizen (0/1)")
    partner: str = Field(..., description="Has partner (Yes/No)")
    dependents: str = Field(..., description="Has dependents (Yes/No)")
    
    # Account (5)
    tenure: int = Field(..., ge=0, description="Tenure in months")
    contract: str = Field(..., description="Contract type (Month-to-month/One year/Two year)")
    paperless_billing: str = Field(..., description="Paperless billing (Yes/No)")
    payment_method: str = Field(..., description="Payment method")
    monthly_charges: float = Field(..., gt=0, description="Monthly charges")
    total_charges: float = Field(..., ge=0, description="Total charges")
    
    # Phone Services (2)
    phone_service: str = Field(..., description="Phone service (Yes/No)")
    multiple_lines: str = Field(..., description="Multiple lines (Yes/No/No phone service)")
    
    # Internet Services (7)
    internet_service: str = Field(..., description="Internet service (DSL/Fiber optic/No)")
    online_security: str = Field(..., description="Online security (Yes/No/No internet service)")
    online_backup: str = Field(..., description="Online backup (Yes/No/No internet service)")
    device_protection: str = Field(..., description="Device protection (Yes/No/No internet service)")
    tech_support: str = Field(..., description="Tech support (Yes/No/No internet service)")
    streaming_tv: str = Field(..., description="Streaming TV (Yes/No/No internet service)")
    streaming_movies: str = Field(..., description="Streaming movies (Yes/No/No internet service)")


class OfferRecommendation(BaseModel):
    """Offer recommendation"""
    campaign_name: str
    discount_percentage: int
    duration: int
    estimated_cost: float
    rationale: str


class PredictionResponse(BaseModel):
    """Risk prediction response"""
    risk_score: float
    risk_level: str
    shap_values: List[ShapFeature]
    ai_analysis: str
    recommended_offer: Optional[OfferRecommendation]


@router.post("/calculate", response_model=PredictionResponse)
async def calculate_risk(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate churn risk for hypothetical customer profile
    
    Args:
        request: Customer features for prediction (TrustedModel format)
        
    Returns:
        Risk score and prediction details
    """
    try:
        # Prepare customer data for predictor
        customer_data = {
            "gender": request.gender,
            "senior_citizen": request.senior_citizen,
            "partner": request.partner,
            "dependents": request.dependents,
            "tenure": request.tenure,
            "contract": request.contract,
            "paperless_billing": request.paperless_billing,
            "payment_method": request.payment_method,
            "monthly_charges": request.monthly_charges,
            "total_charges": request.total_charges,
            "phone_service": request.phone_service,
            "multiple_lines": request.multiple_lines,
            "internet_service": request.internet_service,
            "online_security": request.online_security,
            "online_backup": request.online_backup,
            "device_protection": request.device_protection,
            "tech_support": request.tech_support,
            "streaming_tv": request.streaming_tv,
            "streaming_movies": request.streaming_movies
        }
        
        # Get prediction
        prediction = predictor.predict(customer_data)
        
        # For now, return simplified response without SHAP/offers
        # TODO: Implement SHAP explainer for TrustedModel
        return PredictionResponse(
            risk_score=prediction["churn_probability"],
            risk_level=prediction["risk_level"],
            shap_values=[],  # TODO: Implement SHAP
            ai_analysis=f"Müşteri {prediction['risk_level']} risk seviyesinde. Churn olasılığı: %{prediction['churn_probability']*100:.1f}",
            recommended_offer=None  # TODO: Implement offer optimizer
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Risk hesaplanırken hata oluştu: {str(e)}"
        )
