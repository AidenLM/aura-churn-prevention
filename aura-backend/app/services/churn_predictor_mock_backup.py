import numpy as np
import pandas as pd
from typing import List
from datetime import datetime
from app.schemas.customer import CustomerFeatures, PredictionResult

class ChurnPredictor:
    """
    Churn prediction service using XGBoost model
    
    This service wraps the XGBoost model for churn prediction and provides
    risk level classification based on prediction scores.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize ChurnPredictor with model
        
        Args:
            model_path: Path to trained XGBoost model (optional for now)
        """
        self.model = None
        self.model_path = model_path
        
        # For now, we'll use a mock model until we train a real one
        # In production, this would load: self.model = joblib.load(model_path)
        
    def _classify_risk_level(self, risk_score: float) -> str:
        """
        Classify risk score into risk level categories
        
        Args:
            risk_score: Risk score between 0 and 1
            
        Returns:
            Risk level: 'Low', 'Medium', or 'High'
        """
        if risk_score < 0.3:
            return 'Low'
        elif risk_score < 0.7:
            return 'Medium'
        else:
            return 'High'
    
    def _features_to_array(self, features: CustomerFeatures) -> np.ndarray:
        """
        Convert CustomerFeatures to numpy array for model input
        
        Args:
            features: CustomerFeatures object
            
        Returns:
            Numpy array of feature values
        """
        return np.array([[
            features.tenure,
            1 if features.plan_type == 'Premium' else (0.5 if features.plan_type == 'Standart' else 0),
            features.monthly_charge,
            features.data_usage_gb,
            features.voice_minutes,
            features.sms_count,
            features.complaint_count,
            features.support_calls_count,
            features.payment_delays,
            1 if features.contract_type == 'Annual' else 0
        ]])
    
    def _mock_predict(self, features_array: np.ndarray) -> float:
        """
        Mock prediction function (until real model is trained)
        
        This creates a realistic risk score based on customer features:
        - High complaints, payment delays, low tenure → High risk
        - Low usage, high charges → Medium-High risk
        - Long tenure, no complaints → Low risk
        
        Args:
            features_array: Feature array
            
        Returns:
            Risk score between 0 and 1
        """
        tenure, plan_type, monthly_charge, data_usage, voice_minutes, sms_count, \
            complaints, support_calls, payment_delays, contract_type = features_array[0]
        
        # Base risk
        risk = 0.3
        
        # Tenure factor (longer tenure = lower risk)
        if tenure < 6:
            risk += 0.2
        elif tenure > 24:
            risk -= 0.15
        
        # Complaint factor
        risk += complaints * 0.08
        
        # Payment delays factor
        risk += payment_delays * 0.12
        
        # Support calls factor
        risk += support_calls * 0.03
        
        # Usage factor (low usage = higher risk)
        if data_usage < 5:
            risk += 0.1
        if voice_minutes < 100:
            risk += 0.05
        
        # Contract type (annual = lower risk)
        if contract_type == 1:
            risk -= 0.1
        
        # Price sensitivity (high charge with low usage = higher risk)
        if monthly_charge > 200 and data_usage < 10:
            risk += 0.15
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, risk))
    
    def predict(self, features: CustomerFeatures) -> PredictionResult:
        """
        Generate churn risk prediction for customer features
        
        Args:
            features: CustomerFeatures object with all required fields
            
        Returns:
            PredictionResult with risk_score (0-1) and risk_level
            
        Raises:
            ValueError: If features are invalid
        """
        # Validate features
        if features.tenure < 0:
            raise ValueError("Tenure cannot be negative")
        if features.monthly_charge < 0:
            raise ValueError("Monthly charge cannot be negative")
        
        # Convert to array
        features_array = self._features_to_array(features)
        
        # Get prediction (mock for now)
        if self.model is None:
            risk_score = self._mock_predict(features_array)
        else:
            # Real model prediction
            risk_score = float(self.model.predict_proba(features_array)[0][1])
        
        # Classify risk level
        risk_level = self._classify_risk_level(risk_score)
        
        return PredictionResult(
            risk_score=risk_score,
            risk_level=risk_level,
            timestamp=datetime.now()
        )
    
    def predict_batch(self, features_list: List[CustomerFeatures]) -> List[PredictionResult]:
        """
        Batch prediction for multiple customers
        
        Args:
            features_list: List of CustomerFeatures objects
            
        Returns:
            List of PredictionResult objects
        """
        return [self.predict(features) for features in features_list]
