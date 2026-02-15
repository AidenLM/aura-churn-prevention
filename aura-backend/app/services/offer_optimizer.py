from typing import List, Optional
from pydantic import BaseModel


class Campaign(BaseModel):
    """Campaign catalog model"""
    campaign_id: str
    name_tr: str
    discount_percentage: int
    duration_months: int
    cost_per_customer: float
    target_segments: List[str]
    min_tenure: int
    max_monthly_charge: Optional[float] = None


class OfferRecommendation(BaseModel):
    """Offer recommendation model"""
    campaign_name: str
    discount_percentage: int
    duration: int
    estimated_cost: float
    rationale: str


class OfferOptimizer:
    """
    Offer recommendation service for retention campaigns
    
    This service recommends optimal retention campaigns based on
    customer profile and churn risk level.
    """
    
    # Campaign catalog (in production, this would come from database)
    CAMPAIGNS = [
        Campaign(
            campaign_id="CAMP001",
            name_tr="%30 İndirim Kampanyası",
            discount_percentage=30,
            duration_months=6,
            cost_per_customer=539.97,
            target_segments=["high_risk", "price_sensitive"],
            min_tenure=0,
            max_monthly_charge=400.0
        ),
        Campaign(
            campaign_id="CAMP002",
            name_tr="%20 İndirim + Ekstra 10GB",
            discount_percentage=20,
            duration_months=3,
            cost_per_customer=359.98,
            target_segments=["high_risk", "data_user"],
            min_tenure=0,
            max_monthly_charge=300.0
        ),
        Campaign(
            campaign_id="CAMP003",
            name_tr="Sadakat Bonusu - %15 İndirim",
            discount_percentage=15,
            duration_months=12,
            cost_per_customer=539.96,
            target_segments=["medium_risk", "loyal"],
            min_tenure=12,
            max_monthly_charge=None
        ),
        Campaign(
            campaign_id="CAMP004",
            name_tr="Yeni Müşteri Özel - %25 İndirim",
            discount_percentage=25,
            duration_months=6,
            cost_per_customer=449.97,
            target_segments=["high_risk", "new_customer"],
            min_tenure=0,
            max_monthly_charge=350.0
        ),
        Campaign(
            campaign_id="CAMP005",
            name_tr="Premium Paket İndirimi - %10",
            discount_percentage=10,
            duration_months=6,
            cost_per_customer=539.94,
            target_segments=["medium_risk", "premium"],
            min_tenure=6,
            max_monthly_charge=None
        ),
    ]
    
    def __init__(self, offer_catalog: Optional[List[Campaign]] = None):
        """
        Initialize offer optimizer
        
        Args:
            offer_catalog: List of available campaigns (uses default if None)
        """
        self.offer_catalog = offer_catalog or self.CAMPAIGNS
    
    def recommend(
        self,
        risk_score: float,
        tenure: int,
        monthly_charge: float,
        data_usage_gb: float,
        complaint_count: int,
        payment_delays: int
    ) -> Optional[OfferRecommendation]:
        """
        Recommend best retention offer for customer
        
        Args:
            risk_score: Churn risk score (0-1)
            tenure: Customer tenure in months
            monthly_charge: Monthly charge amount
            data_usage_gb: Data usage in GB
            complaint_count: Number of complaints
            payment_delays: Number of payment delays
            
        Returns:
            OfferRecommendation if risk is high, None otherwise
        """
        # Only recommend for high-risk customers (>= 0.7)
        if risk_score < 0.7:
            return None
        
        # Determine customer segment
        segments = self._determine_segments(
            risk_score, tenure, monthly_charge, data_usage_gb, 
            complaint_count, payment_delays
        )
        
        # Filter campaigns by profile constraints
        suitable_campaigns = self._filter_campaigns(
            segments, tenure, monthly_charge
        )
        
        if not suitable_campaigns:
            # Fallback to default high-risk campaign
            suitable_campaigns = [self.CAMPAIGNS[0]]
        
        # Rank by expected effectiveness
        ranked_campaigns = self._rank_campaigns(
            suitable_campaigns, segments, risk_score
        )
        
        # Select best campaign
        best_campaign = ranked_campaigns[0]
        
        # Generate Turkish rationale
        rationale = self._generate_rationale(
            best_campaign, segments, risk_score, monthly_charge, 
            complaint_count, payment_delays
        )
        
        return OfferRecommendation(
            campaign_name=best_campaign.name_tr,
            discount_percentage=best_campaign.discount_percentage,
            duration=best_campaign.duration_months,
            estimated_cost=best_campaign.cost_per_customer,
            rationale=rationale
        )
    
    def _determine_segments(
        self,
        risk_score: float,
        tenure: int,
        monthly_charge: float,
        data_usage_gb: float,
        complaint_count: int,
        payment_delays: int
    ) -> List[str]:
        """Determine customer segments based on profile"""
        segments = []
        
        # Risk level
        if risk_score >= 0.7:
            segments.append("high_risk")
        elif risk_score >= 0.3:
            segments.append("medium_risk")
        
        # Tenure-based
        if tenure < 6:
            segments.append("new_customer")
        elif tenure >= 24:
            segments.append("loyal")
        
        # Price sensitivity
        if payment_delays > 0 or monthly_charge > 250:
            segments.append("price_sensitive")
        
        # Usage patterns
        if data_usage_gb > 15:
            segments.append("data_user")
        
        # Plan type
        if monthly_charge > 250:
            segments.append("premium")
        
        return segments
    
    def _filter_campaigns(
        self,
        segments: List[str],
        tenure: int,
        monthly_charge: float
    ) -> List[Campaign]:
        """Filter campaigns by profile constraints"""
        suitable = []
        
        for campaign in self.offer_catalog:
            # Check tenure requirement
            if tenure < campaign.min_tenure:
                continue
            
            # Check monthly charge limit
            if campaign.max_monthly_charge and monthly_charge > campaign.max_monthly_charge:
                continue
            
            # Check segment match
            if any(seg in campaign.target_segments for seg in segments):
                suitable.append(campaign)
        
        return suitable
    
    def _rank_campaigns(
        self,
        campaigns: List[Campaign],
        segments: List[str],
        risk_score: float
    ) -> List[Campaign]:
        """Rank campaigns by expected effectiveness"""
        def effectiveness_score(campaign: Campaign) -> float:
            score = 0.0
            
            # Higher discount = more effective for high risk
            score += campaign.discount_percentage * 0.3
            
            # Segment match count
            segment_matches = sum(1 for seg in segments if seg in campaign.target_segments)
            score += segment_matches * 20
            
            # Shorter duration = more attractive
            score += (12 - campaign.duration_months) * 2
            
            # Risk-specific weighting
            if risk_score >= 0.8:
                # Very high risk: prioritize aggressive discounts
                score += campaign.discount_percentage * 0.5
            
            return score
        
        return sorted(campaigns, key=effectiveness_score, reverse=True)
    
    def _generate_rationale(
        self,
        campaign: Campaign,
        segments: List[str],
        risk_score: float,
        monthly_charge: float,
        complaint_count: int,
        payment_delays: int
    ) -> str:
        """Generate natural language rationale in Turkish"""
        reasons = []
        
        # Price sensitivity
        if "price_sensitive" in segments or payment_delays > 0:
            if monthly_charge > 250:
                reasons.append("Yüksek aylık fatura nedeniyle fiyat hassasiyeti gösteriyor")
            if payment_delays > 0:
                reasons.append("Ödeme gecikmeleri maliyet endişesi işareti")
        
        # Complaints
        if complaint_count > 2:
            reasons.append("Şikayetler nedeniyle memnuniyetsizlik var")
        
        # New customer
        if "new_customer" in segments:
            reasons.append("Yeni müşteri olduğu için rakip tekliflere açık")
        
        # High risk
        if risk_score >= 0.8:
            reasons.append("Çok yüksek kayıp riski acil müdahale gerektiriyor")
        
        # Data usage
        if "data_user" in segments:
            reasons.append("Yoğun veri kullanıcısı için ekstra GB cazip olabilir")
        
        # Loyal customer
        if "loyal" in segments:
            reasons.append("Uzun süreli müşteri sadakat ödülü hak ediyor")
        
        if reasons:
            return ". ".join(reasons) + "."
        else:
            return f"{campaign.discount_percentage}% indirim müşteri kaybını önlemeye yardımcı olacak."
