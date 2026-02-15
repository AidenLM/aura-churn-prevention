"""ROI Simulation API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.base import get_db
from app.repositories.customer_repository import CustomerRepository
from app.services.roi_simulator import ROISimulator

router = APIRouter(prefix="/api/simulation", tags=["simulation"])

# Initialize simulator
simulator = ROISimulator()


class SimulationRequest(BaseModel):
    """ROI simulation request"""
    risk_threshold: float = Field(..., ge=0.0, le=1.0, description="Risk threshold (0-1)")
    campaign_budget: float = Field(..., gt=0, description="Campaign budget in TL")


class SimulationResponse(BaseModel):
    """ROI simulation response"""
    targeted_customers: int
    cost_per_customer: float
    total_cost: float
    expected_retention_rate: float
    projected_revenue: float
    roi: float
    net_gain: float
    coverage_percentage: float


@router.post("/roi", response_model=SimulationResponse)
async def simulate_roi(
    request: SimulationRequest,
    db: Session = Depends(get_db)
):
    """
    Simulate campaign ROI for given parameters
    
    Args:
        request: Simulation parameters (risk threshold and budget)
        
    Returns:
        Complete ROI analysis with all metrics
    """
    try:
        repo = CustomerRepository(db)
        
        # Get current statistics
        stats = repo.get_summary_stats()
        
        # Run simulation
        result = simulator.simulate(
            risk_threshold=request.risk_threshold,
            campaign_budget=request.campaign_budget,
            total_customers=stats.total_customers,
            risk_distribution=stats.risk_distribution
        )
        
        return SimulationResponse(
            targeted_customers=result.targeted_customers,
            cost_per_customer=result.cost_per_customer,
            total_cost=result.total_cost,
            expected_retention_rate=result.expected_retention_rate,
            projected_revenue=result.projected_revenue,
            roi=result.roi,
            net_gain=result.net_gain,
            coverage_percentage=result.coverage_percentage
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ROI simülasyonu çalıştırılırken hata oluştu: {str(e)}"
        )
