"""Dashboard API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel

from app.db.base import get_db
from app.repositories.customer_repository import CustomerRepository

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


class CustomerRiskData(BaseModel):
    """Customer risk data for dashboard"""
    customer_id: str
    name: str
    risk_score: float
    risk_level: str


class DashboardSummaryResponse(BaseModel):
    """Dashboard summary statistics response"""
    total_customers: int
    high_risk_count: int
    average_risk: float
    monthly_churn_rate: float
    risk_distribution: Dict[str, int]
    top_risky_customers: List[CustomerRiskData]


@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get dashboard summary statistics
    
    Returns:
        - Total customers count
        - High-risk customers count
        - Average risk score
        - Monthly churn rate
        - Risk distribution (low/medium/high)
        - Top risky customers list
    """
    try:
        repo = CustomerRepository(db)
        
        # Get summary statistics
        stats = repo.get_summary_stats()
        
        # Get top risky customers
        high_risk_customers = repo.get_high_risk_customers(limit=limit)
        
        # Build top risky customers list
        top_risky = []
        for customer in high_risk_customers:
            # Get latest prediction
            prediction = repo.get_latest_prediction(customer.customer_id)
            if prediction:
                top_risky.append(CustomerRiskData(
                    customer_id=customer.customer_id,
                    name=customer.customer_id,  # Using customer_id as name
                    risk_score=float(prediction.risk_score),
                    risk_level=prediction.risk_level
                ))
        
        return DashboardSummaryResponse(
            total_customers=stats.total_customers,
            high_risk_count=stats.high_risk_count,
            average_risk=stats.average_risk,
            monthly_churn_rate=stats.monthly_churn_rate,
            risk_distribution=stats.risk_distribution,
            top_risky_customers=top_risky
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Dashboard verisi alınırken hata oluştu: {str(e)}"
        )
