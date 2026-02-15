from typing import Dict
from pydantic import BaseModel


class SimulationResult(BaseModel):
    """ROI simulation result model"""
    targeted_customers: int
    cost_per_customer: float
    total_cost: float
    expected_retention_rate: float
    projected_revenue: float
    roi: float  # percentage
    net_gain: float
    coverage_percentage: float


class ROISimulator:
    """
    ROI simulation service for retention campaigns
    
    This service calculates campaign ROI and budget scenarios
    based on risk thresholds and budget constraints.
    """
    
    def __init__(
        self,
        avg_customer_ltv: float = 2500.0,  # Average customer lifetime value (₺)
        base_retention_rate: float = 0.35,  # Base retention without campaign
        campaign_effectiveness: float = 0.65  # Campaign success rate
    ):
        """
        Initialize ROI simulator
        
        Args:
            avg_customer_ltv: Average customer lifetime value in Turkish Lira
            base_retention_rate: Base retention rate without intervention
            campaign_effectiveness: Campaign success rate (0-1)
        """
        self.avg_customer_ltv = avg_customer_ltv
        self.base_retention_rate = base_retention_rate
        self.campaign_effectiveness = campaign_effectiveness
    
    def simulate(
        self,
        risk_threshold: float,
        campaign_budget: float,
        total_customers: int,
        risk_distribution: Dict[str, int]
    ) -> SimulationResult:
        """
        Simulate campaign ROI for given parameters
        
        Args:
            risk_threshold: Minimum risk score to target (0-1)
            campaign_budget: Total budget in Turkish Lira
            total_customers: Total customer base size
            risk_distribution: Count of customers by risk level
                              {"low": count, "medium": count, "high": count}
            
        Returns:
            SimulationResult with ROI metrics
        """
        # Calculate targeted customers based on risk threshold
        targeted_customers = self._calculate_targeted_customers(
            risk_threshold, risk_distribution
        )
        
        if targeted_customers == 0:
            # No customers to target
            return SimulationResult(
                targeted_customers=0,
                cost_per_customer=0.0,
                total_cost=0.0,
                expected_retention_rate=0.0,
                projected_revenue=0.0,
                roi=0.0,
                net_gain=0.0,
                coverage_percentage=0.0
            )
        
        # Calculate cost per customer
        cost_per_customer = campaign_budget / targeted_customers
        
        # Total cost (capped at budget)
        total_cost = min(campaign_budget, cost_per_customer * targeted_customers)
        
        # Expected retention rate (campaign effectiveness)
        expected_retention_rate = self.campaign_effectiveness
        
        # Calculate retained customers
        retained_customers = int(targeted_customers * expected_retention_rate)
        
        # Projected revenue (retained customers * LTV)
        projected_revenue = retained_customers * self.avg_customer_ltv
        
        # ROI calculation: ((Revenue - Cost) / Cost) * 100
        if total_cost > 0:
            roi = ((projected_revenue - total_cost) / total_cost) * 100
        else:
            roi = 0.0
        
        # Net gain
        net_gain = projected_revenue - total_cost
        
        # Coverage percentage
        coverage_percentage = (targeted_customers / total_customers) * 100
        
        return SimulationResult(
            targeted_customers=targeted_customers,
            cost_per_customer=cost_per_customer,
            total_cost=total_cost,
            expected_retention_rate=expected_retention_rate,
            projected_revenue=projected_revenue,
            roi=roi,
            net_gain=net_gain,
            coverage_percentage=coverage_percentage
        )
    
    def _calculate_targeted_customers(
        self,
        risk_threshold: float,
        risk_distribution: Dict[str, int]
    ) -> int:
        """
        Calculate number of customers to target based on risk threshold
        
        Args:
            risk_threshold: Minimum risk score (0-1)
            risk_distribution: Customer counts by risk level
            
        Returns:
            Number of customers with risk >= threshold
        """
        targeted = 0
        
        # High risk: 0.7-1.0
        if risk_threshold <= 0.7:
            targeted += risk_distribution.get("high", 0)
        
        # Medium risk: 0.3-0.7
        if risk_threshold <= 0.3:
            targeted += risk_distribution.get("medium", 0)
        
        # Low risk: 0-0.3
        if risk_threshold <= 0.0:
            targeted += risk_distribution.get("low", 0)
        
        # If threshold is between ranges, estimate proportionally
        if 0.3 < risk_threshold < 0.7:
            # Partial medium risk customers
            medium_count = risk_distribution.get("medium", 0)
            # Estimate: assume uniform distribution within medium range
            proportion = (0.7 - risk_threshold) / 0.4
            targeted += int(medium_count * proportion)
            # All high risk
            targeted += risk_distribution.get("high", 0)
        elif 0.0 < risk_threshold < 0.3:
            # Partial low risk customers
            low_count = risk_distribution.get("low", 0)
            proportion = (0.3 - risk_threshold) / 0.3
            targeted += int(low_count * proportion)
            # All medium and high
            targeted += risk_distribution.get("medium", 0)
            targeted += risk_distribution.get("high", 0)
        
        return targeted
    
    def calculate_optimal_budget(
        self,
        target_roi: float,
        total_customers: int,
        risk_distribution: Dict[str, int],
        risk_threshold: float = 0.7
    ) -> float:
        """
        Calculate optimal budget to achieve target ROI
        
        Args:
            target_roi: Desired ROI percentage
            total_customers: Total customer base
            risk_distribution: Customer counts by risk level
            risk_threshold: Risk threshold for targeting
            
        Returns:
            Recommended budget in Turkish Lira
        """
        targeted_customers = self._calculate_targeted_customers(
            risk_threshold, risk_distribution
        )
        
        if targeted_customers == 0:
            return 0.0
        
        # Work backwards from target ROI
        # ROI = ((Revenue - Cost) / Cost) * 100
        # Revenue = retained_customers * LTV
        # retained_customers = targeted * effectiveness
        
        retained = targeted_customers * self.campaign_effectiveness
        revenue = retained * self.avg_customer_ltv
        
        # Solve for cost: ROI = ((Revenue - Cost) / Cost) * 100
        # Cost = Revenue / (1 + ROI/100)
        optimal_cost = revenue / (1 + target_roi / 100)
        
        return optimal_cost
