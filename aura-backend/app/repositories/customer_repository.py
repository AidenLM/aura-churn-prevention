from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from pydantic import BaseModel

from app.db.models import Customer, PredictionRecord
from app.core.cache import cache


class SummaryStats(BaseModel):
    """Dashboard summary statistics"""
    total_customers: int
    high_risk_count: int
    average_risk: float
    monthly_churn_rate: float
    risk_distribution: Dict[str, int]


class CustomerRepository:
    """
    Data access layer for customer information
    
    Provides methods for retrieving, querying, and managing customer data
    and prediction records.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize repository with database session
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    def get_by_id(self, customer_id: str, use_cache: bool = True) -> Optional[Customer]:
        """
        Retrieve customer by ID
        
        Args:
            customer_id: Customer ID to retrieve
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Customer object if found, None otherwise
        """
        # Check cache first
        if use_cache:
            cache_key = f"customer:{customer_id}"
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
        
        # Query database
        customer = self.db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
        
        # Cache result (5 minutes TTL)
        if customer and use_cache:
            cache.set(cache_key, customer, ttl_seconds=300)
        
        return customer
    
    def get_high_risk_customers(self, limit: int = 10) -> List[Customer]:
        """
        Get customers with high risk scores
        
        This queries the most recent predictions and returns customers
        with risk_level = 'High', ordered by risk score descending.
        
        Args:
            limit: Maximum number of customers to return
            
        Returns:
            List of Customer objects with high risk
        """
        # Subquery to get latest prediction for each customer
        latest_predictions = (
            self.db.query(
                PredictionRecord.customer_id,
                func.max(PredictionRecord.timestamp).label('max_timestamp')
            )
            .group_by(PredictionRecord.customer_id)
            .subquery()
        )
        
        # Join to get customers with high risk
        high_risk_customers = (
            self.db.query(Customer)
            .join(
                PredictionRecord,
                Customer.customer_id == PredictionRecord.customer_id
            )
            .join(
                latest_predictions,
                (PredictionRecord.customer_id == latest_predictions.c.customer_id) &
                (PredictionRecord.timestamp == latest_predictions.c.max_timestamp)
            )
            .filter(PredictionRecord.risk_level == 'High')
            .order_by(desc(PredictionRecord.risk_score))
            .limit(limit)
            .all()
        )
        
        return high_risk_customers
    
    def get_random_customer(self) -> Optional[Customer]:
        """
        Get random customer for demo purposes
        
        Returns:
            Random Customer object, or None if no customers exist
        """
        # Use ORDER BY RANDOM() for SQLite, RAND() for MySQL, random() for PostgreSQL
        # SQLite syntax (current database)
        return self.db.query(Customer).order_by(func.random()).first()
    
    def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """
        Get all customers with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Customer objects
        """
        return self.db.query(Customer).offset(skip).limit(limit).all()
    
    def get_summary_stats(self, use_cache: bool = True) -> SummaryStats:
        """
        Calculate dashboard summary statistics
        
        Args:
            use_cache: Whether to use cache (default: True)
        
        Returns:
            SummaryStats with total customers, risk counts, and distribution
        """
        # Check cache first
        if use_cache:
            cache_key = "summary_stats"
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
        
        # Total customers
        total_customers = self.db.query(func.count(Customer.customer_id)).scalar() or 0
        
        if total_customers == 0:
            return SummaryStats(
                total_customers=0,
                high_risk_count=0,
                average_risk=0.0,
                monthly_churn_rate=0.0,
                risk_distribution={"low": 0, "medium": 0, "high": 0}
            )
        
        # Get latest predictions for risk statistics
        latest_predictions_subquery = (
            self.db.query(
                PredictionRecord.customer_id,
                func.max(PredictionRecord.timestamp).label('max_timestamp')
            )
            .group_by(PredictionRecord.customer_id)
            .subquery()
        )
        
        latest_predictions = (
            self.db.query(PredictionRecord)
            .join(
                latest_predictions_subquery,
                (PredictionRecord.customer_id == latest_predictions_subquery.c.customer_id) &
                (PredictionRecord.timestamp == latest_predictions_subquery.c.max_timestamp)
            )
            .all()
        )
        
        # Calculate statistics
        if latest_predictions:
            high_risk_count = sum(1 for p in latest_predictions if p.risk_level == 'High')
            medium_risk_count = sum(1 for p in latest_predictions if p.risk_level == 'Medium')
            low_risk_count = sum(1 for p in latest_predictions if p.risk_level == 'Low')
            
            # Average risk score
            total_risk = sum(float(p.risk_score) for p in latest_predictions)
            average_risk = total_risk / len(latest_predictions)
            
            # Monthly churn rate (estimated as percentage of high-risk customers)
            monthly_churn_rate = (high_risk_count / total_customers) * 100 * 0.3  # 30% of high-risk actually churn
        else:
            # No predictions yet - return defaults
            high_risk_count = 0
            medium_risk_count = 0
            low_risk_count = 0
            average_risk = 0.0
            monthly_churn_rate = 0.0
        
        stats = SummaryStats(
            total_customers=total_customers,
            high_risk_count=high_risk_count,
            average_risk=round(average_risk, 2),
            monthly_churn_rate=round(monthly_churn_rate, 1),
            risk_distribution={
                "low": low_risk_count,
                "medium": medium_risk_count,
                "high": high_risk_count
            }
        )
        
        # Cache result (5 minutes TTL)
        if use_cache:
            cache.set("summary_stats", stats, ttl_seconds=300)
        
        return stats
    
    def save_prediction(
        self,
        customer_id: str,
        risk_score: float,
        risk_level: str,
        shap_values: dict = None,
        user_id: Optional[str] = None
    ) -> PredictionRecord:
        """
        Store prediction in audit trail
        
        Args:
            customer_id: Customer ID
            risk_score: Predicted risk score (0-1)
            risk_level: Risk level classification (Low/Medium/High)
            shap_values: SHAP feature importance values as dict (optional, not stored)
            user_id: Optional user ID who made the prediction
            
        Returns:
            Created PredictionRecord object
        """
        predicted_churn = "Yes" if risk_score >= 0.5 else "No"
        
        prediction = PredictionRecord(
            customer_id=customer_id,
            churn_probability=risk_score,
            risk_score=risk_score,  # Same as churn_probability
            risk_level=risk_level,
            predicted_churn=predicted_churn,
            model_name="Voting Classifier",
            user_id=user_id,
            timestamp=datetime.utcnow()
        )
        
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        
        return prediction
    
    def get_customer_prediction_history(
        self,
        customer_id: str,
        limit: int = 10
    ) -> List[PredictionRecord]:
        """
        Get prediction history for a customer
        
        Args:
            customer_id: Customer ID
            limit: Maximum number of records to return
            
        Returns:
            List of PredictionRecord objects, ordered by timestamp descending
        """
        return (
            self.db.query(PredictionRecord)
            .filter(PredictionRecord.customer_id == customer_id)
            .order_by(desc(PredictionRecord.timestamp))
            .limit(limit)
            .all()
        )
    
    def get_latest_prediction(self, customer_id: str) -> Optional[PredictionRecord]:
        """
        Get most recent prediction for a customer
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Latest PredictionRecord or None if no predictions exist
        """
        return (
            self.db.query(PredictionRecord)
            .filter(PredictionRecord.customer_id == customer_id)
            .order_by(desc(PredictionRecord.timestamp))
            .first()
        )
    
    def create_customer(self, customer_data: dict) -> Customer:
        """
        Create a new customer
        
        Args:
            customer_data: Dictionary with customer fields
            
        Returns:
            Created Customer object
        """
        customer = Customer(**customer_data)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def update_customer(self, customer_id: str, customer_data: dict) -> Optional[Customer]:
        """
        Update existing customer
        
        Args:
            customer_id: Customer ID to update
            customer_data: Dictionary with fields to update
            
        Returns:
            Updated Customer object or None if not found
        """
        customer = self.get_by_id(customer_id, use_cache=False)
        if not customer:
            return None
        
        for key, value in customer_data.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        
        self.db.commit()
        self.db.refresh(customer)
        
        # Invalidate cache for this customer
        cache.delete(f"customer:{customer_id}")
        cache.delete("summary_stats")
        
        return customer
    
    def delete_customer(self, customer_id: str) -> bool:
        """
        Delete a customer
        
        Args:
            customer_id: Customer ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        customer = self.get_by_id(customer_id)
        if not customer:
            return False
        
        self.db.delete(customer)
        self.db.commit()
        return True
    
    def count_customers(self) -> int:
        """
        Get total customer count
        
        Returns:
            Total number of customers
        """
        return self.db.query(func.count(Customer.customer_id)).scalar() or 0
