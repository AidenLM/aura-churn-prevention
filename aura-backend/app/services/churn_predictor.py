"""
Churn Predictor Service - TrustedModel Implementation
Uses Voting Classifier (Random Forest + Gradient Boosting + Logistic Regression)
"""
import pickle
import numpy as np
from typing import Dict, List
import os

class ChurnPredictor:
    """Churn prediction service using TrustedModel"""
    
    def __init__(self, model_path: str = None):
        """Initialize the predictor with trained model"""
        if model_path is None:
            # Get absolute path to models directory
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            model_path = os.path.join(base_dir, "models")
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.metadata = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model, scaler, and feature names"""
        try:
            # Get absolute path relative to this file
            import os
            
            # This file is at: aura-backend/app/services/churn_predictor.py
            # We nee
            # Load model
            model_file = os.path.join(model_dir, "best_model.pkl")
            print(f"Loading model from: {model_file}")
            with open(model_file, "rb") as f:
                self.model = pickle.load(f)
            
            # Load scaler
            scaler_file = os.path.join(model_dir, "scaler.pkl")
            with open(scaler_file, "rb") as f:
                self.scaler = pickle.load(f)
            
            # Load feature names
            features_file = os.path.join(model_dir, "feature_names.pkl")
            with open(features_file, "rb") as f:
                self.feature_names = pickle.load(f)
            
            # Load metadata
            import json
            metadata_file = os.path.join(model_dir, "model_metadata.json")
            with open(metadata_file, "r") as f:
                self.metadata = json.load(f)
            
            print(f"✅ Model loaded: {self.metadata['model_name']}")
            print(f"   Accuracy: {self.metadata['accuracy']:.4f}")
            print(f"   ROC-AUC: {self.metadata['roc_auc']:.4f}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def _prepare_features(self, customer_data: Dict) -> np.ndarray:
        """
        Prepare customer features for prediction
        
        Expected features (19):
        1. gender (encoded)
        2. SeniorCitizen (0 or 1)
        3. Partner (encoded)
        4. Dependents (encoded)
        5. tenure (scaled)
        6. PhoneService (encoded)
        7. MultipleLines (encoded)
        8. InternetService (encoded)
        9. OnlineSecurity (encoded)
        10. OnlineBackup (encoded)
        11. DeviceProtection (encoded)
        12. TechSupport (encoded)
        13. StreamingTV (encoded)
        14. StreamingMovies (encoded)
        15. Contract (encoded)
        16. PaperlessBilling (encoded)
        17. PaymentMethod (encoded)
        18. MonthlyCharges (scaled)
        19. TotalCharges (scaled)
        """
        
        # Encoding mappings (same as training)
        gender_map = {'Female': 0, 'Male': 1}
        yes_no_map = {'No': 0, 'Yes': 1}
        multiple_lines_map = {'No': 0, 'No phone service': 1, 'Yes': 2}
        internet_map = {'DSL': 0, 'Fiber optic': 1, 'No': 2}
        internet_service_map = {'No': 0, 'No internet service': 1, 'Yes': 2}
        contract_map = {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
        payment_map = {
            'Bank transfer (automatic)': 0,
            'Credit card (automatic)': 1,
            'Electronic check': 2,
            'Mailed check': 3
        }
        
        # Extract and encode features
        features = []
        
        # 1. gender
        features.append(gender_map.get(customer_data.get('gender', 'Male'), 1))
        
        # 2. SeniorCitizen
        features.append(customer_data.get('senior_citizen', 0))
        
        # 3. Partner
        features.append(yes_no_map.get(customer_data.get('partner', 'No'), 0))
        
        # 4. Dependents
        features.append(yes_no_map.get(customer_data.get('dependents', 'No'), 0))
        
        # 5. tenure (will be scaled)
        features.append(customer_data.get('tenure', 0))
        
        # 6. PhoneService
        features.append(yes_no_map.get(customer_data.get('phone_service', 'No'), 0))
        
        # 7. MultipleLines
        features.append(multiple_lines_map.get(customer_data.get('multiple_lines', 'No'), 0))
        
        # 8. InternetService
        features.append(internet_map.get(customer_data.get('internet_service', 'No'), 2))
        
        # 9. OnlineSecurity
        features.append(internet_service_map.get(customer_data.get('online_security', 'No'), 0))
        
        # 10. OnlineBackup
        features.append(internet_service_map.get(customer_data.get('online_backup', 'No'), 0))
        
        # 11. DeviceProtection
        features.append(internet_service_map.get(customer_data.get('device_protection', 'No'), 0))
        
        # 12. TechSupport
        features.append(internet_service_map.get(customer_data.get('tech_support', 'No'), 0))
        
        # 13. StreamingTV
        features.append(internet_service_map.get(customer_data.get('streaming_tv', 'No'), 0))
        
        # 14. StreamingMovies
        features.append(internet_service_map.get(customer_data.get('streaming_movies', 'No'), 0))
        
        # 15. Contract
        features.append(contract_map.get(customer_data.get('contract', 'Month-to-month'), 0))
        
        # 16. PaperlessBilling
        features.append(yes_no_map.get(customer_data.get('paperless_billing', 'No'), 0))
        
        # 17. PaymentMethod
        features.append(payment_map.get(customer_data.get('payment_method', 'Electronic check'), 2))
        
        # 18. MonthlyCharges (will be scaled)
        features.append(customer_data.get('monthly_charges', 0.0))
        
        # 19. TotalCharges (will be scaled)
        features.append(customer_data.get('total_charges', 0.0))
        
        # Convert to numpy array
        features_array = np.array(features).reshape(1, -1)
        
        # Scale only numeric features (indices 4, 17, 18 = tenure, MonthlyCharges, TotalCharges)
        # The scaler was trained on only these 3 features
        numeric_features = features_array[:, [4, 17, 18]]  # Extract numeric columns
        numeric_scaled = self.scaler.transform(numeric_features)
        
        # Replace numeric features with scaled versions
        features_array[:, [4, 17, 18]] = numeric_scaled
        
        return features_array
    
    def predict(self, customer_data: Dict) -> Dict:
        """
        Predict churn probability for a single customer
        
        Args:
            customer_data: Dictionary with customer features
        
        Returns:
            Dictionary with prediction results
        """
        # Prepare features
        features = self._prepare_features(customer_data)
        
        # Get prediction probability
        churn_probability = self.model.predict_proba(features)[0][1]
        
        # Get binary prediction
        predicted_churn = "Yes" if churn_probability >= 0.5 else "No"
        
        # Determine risk level
        if churn_probability >= 0.7:
            risk_level = "High"
        elif churn_probability >= 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            "customer_id": customer_data.get("customer_id", "unknown"),
            "churn_probability": float(churn_probability),
            "predicted_churn": predicted_churn,
            "risk_level": risk_level,
            "model_name": self.metadata["model_name"],
            "tenure": customer_data.get("tenure", 0),
            "monthly_charges": customer_data.get("monthly_charges", 0.0),
            "contract": customer_data.get("contract", "Unknown"),
            "internet_service": customer_data.get("internet_service", "Unknown")
        }
    
    def predict_batch(self, customers_data: List[Dict]) -> List[Dict]:
        """
        Predict churn probability for multiple customers
        
        Args:
            customers_data: List of customer data dictionaries
        
        Returns:
            List of prediction results
        """
        predictions = []
        for customer_data in customers_data:
            try:
                prediction = self.predict(customer_data)
                predictions.append(prediction)
            except Exception as e:
                print(f"Error predicting for customer {customer_data.get('customer_id')}: {e}")
                predictions.append({
                    "customer_id": customer_data.get("customer_id", "unknown"),
                    "error": str(e)
                })
        
        return predictions
    
    def get_model_info(self) -> Dict:
        """Get model metadata"""
        return self.metadata


# Global predictor instance
_predictor = None

def get_predictor() -> ChurnPredictor:
    """Get or create the global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = ChurnPredictor()
    return _predictor
