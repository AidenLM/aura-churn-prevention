"""
Real SHAP-based Explainer - Iranian Dataset Model

Uses SHAP library to explain predictions from Iranian model.
Model features: call_failures, complains, tenure_months, monthly_charge,
                seconds_of_use, frequency_of_use, sms_count, distinct_called_numbers,
                tariff_plan, status, age (11 features)
"""

import numpy as np
import joblib
import shap
from typing import List
from app.schemas.customer import CustomerFeatures, ShapFeature, ShapExplanation


class ShapExplainer:
    """
    Real SHAP explainability service for Iranian dataset model
    """
    
    # Turkish feature name mappings for Iranian model (11 features)
    FEATURE_NAMES_TR = {
        'Call  Failure': 'Başarısız Aramalar',
        'Complains': 'Şikayetler',
        'Subscription  Length': 'Üyelik Süresi (Ay)',
        'Charge  Amount': 'Aylık Fatura (₺)',
        'Seconds of Use': 'Kullanım Süresi (sn)',
        'Frequency of use': 'Kullanım Sıklığı',
        'Frequency of SMS': 'SMS Sayısı',
        'Distinct Called Numbers': 'Farklı Aranan Numara',
        'Tariff Plan': 'Tarife Planı',
        'Status': 'Müşteri Durumu',
        'Age': 'Yaş'
    }
    
    def __init__(self, model_path: str = 'models/churn_model.pkl'):
        """
        Initialize SHAP explainer with trained model
        
        Args:
            model_path: Path to trained model
        """
        try:
            # Load model
            self.model = joblib.load(model_path)
            
            # Load scaler
            self.scaler = joblib.load('models/scaler.pkl')
            
            # Load feature names
            self.feature_names = joblib.load('models/feature_names.pkl')
            
            # Initialize SHAP explainer
            # For tree-based models, use TreeExplainer (fast and exact)
            self.explainer = shap.TreeExplainer(self.model)
            
            print("✅ Iranian Dataset model SHAP explainer initialized")
            print(f"   Features: {self.feature_names}")
            
        except FileNotFoundError as e:
            print(f"⚠️  Trained model not found: {e}")
            print("⚠️  Falling back to mock SHAP values.")
            self.model = None
            self.explainer = None
            self.scaler = None
            self.feature_names = None
    
    def _mock_shap_values(self, features: CustomerFeatures, risk_score: float) -> dict:
        """
        Generate mock SHAP values (fallback) for Iranian model features
        """
        shap_values = {}
        
        # Call failures impact
        if features.call_failures > 0:
            shap_values['call_failures'] = features.call_failures * 0.10
        
        # Complaint count impact
        if features.complaint_count > 0:
            shap_values['complaint_count'] = features.complaint_count * 0.08
        
        # Tenure impact
        if features.tenure < 6:
            shap_values['tenure_months'] = 0.15
        elif features.tenure > 24:
            shap_values['tenure_months'] = -0.12
        
        # Monthly charge impact
        if features.monthly_charge > 200 and features.data_usage_gb < 10:
            shap_values['monthly_charge'] = 0.15
        elif features.monthly_charge < 100:
            shap_values['monthly_charge'] = -0.05
        
        # Seconds of use impact (approximated from voice_minutes)
        seconds_of_use = features.voice_minutes * 60
        if seconds_of_use < 6000:  # Less than 100 minutes
            shap_values['seconds_of_use'] = 0.08
        elif seconds_of_use > 30000:  # More than 500 minutes
            shap_values['seconds_of_use'] = -0.06
        
        # Frequency of use impact (approximated from data_usage_gb)
        if features.data_usage_gb < 5:
            shap_values['frequency_of_use'] = 0.10
        elif features.data_usage_gb > 20:
            shap_values['frequency_of_use'] = -0.08
        
        # SMS count impact
        if features.sms_count < 50:
            shap_values['sms_count'] = 0.05
        elif features.sms_count > 200:
            shap_values['sms_count'] = -0.04
        
        # Distinct called numbers impact (approximated from support_calls_count)
        distinct_numbers = features.support_calls_count + 10
        if distinct_numbers < 15:
            shap_values['distinct_called_numbers'] = 0.07
        elif distinct_numbers > 30:
            shap_values['distinct_called_numbers'] = -0.05
        
        # Age impact
        if features.age < 25:
            shap_values['age'] = 0.06
        elif features.age > 55:
            shap_values['age'] = -0.05
        
        # Tariff plan impact (using gender as proxy)
        if features.gender == 0:  # Female
            shap_values['tariff_plan'] = 0.02
        else:  # Male
            shap_values['tariff_plan'] = -0.02
        
        return shap_values
    
    def _features_to_model_input(self, features: CustomerFeatures) -> np.ndarray:
        """
        Convert CustomerFeatures to model input format
        
        Iranian model uses 11 features in this exact order:
        [call_failures, complains, tenure_months, monthly_charge, seconds_of_use,
         frequency_of_use, sms_count, distinct_called_numbers, tariff_plan, status, age]
        
        Args:
            features: CustomerFeatures to convert
            
        Returns:
            Numpy array ready for model
        """
        feature_array = np.array([[
            features.call_failures,                    # call_failures
            features.complaint_count,                  # complains
            features.tenure,                           # tenure_months
            features.monthly_charge,                   # monthly_charge
            features.voice_minutes * 60,               # seconds_of_use (approximation)
            features.data_usage_gb * 10,               # frequency_of_use (approximation)
            features.sms_count,                        # sms_count
            features.support_calls_count + 10,         # distinct_called_numbers (approximation)
            features.gender,                           # tariff_plan (using gender as proxy)
            features.payment_delays,                   # status (using payment_delays as proxy)
            features.age                               # age
        ]])
        
        return feature_array
    
    def explain(self, features: CustomerFeatures, risk_score: float) -> ShapExplanation:
        """
        Generate SHAP values for customer features
        
        Args:
            features: CustomerFeatures to explain
            risk_score: Predicted risk score
            
        Returns:
            ShapExplanation with feature importances and base value
        """
        if self.explainer is not None:
            try:
                # Convert features to model input
                features_array = self._features_to_model_input(features)
                
                # Scale features
                features_scaled = self.scaler.transform(features_array)
                
                # Get SHAP values
                shap_values = self.explainer.shap_values(features_scaled)
                
                # Convert to ShapFeature objects
                shap_features = []
                for i, (feature_name, shap_value) in enumerate(zip(self.feature_names, shap_values[0])):
                    # Only include features with significant impact
                    if abs(shap_value) > 0.01:
                        shap_features.append(ShapFeature(
                            feature_name=feature_name,
                            importance=abs(shap_value),
                            direction='positive' if shap_value > 0 else 'negative',
                            display_name_tr=self.FEATURE_NAMES_TR.get(feature_name, feature_name)
                        ))
                
                # Sort by absolute importance
                shap_features.sort(key=lambda x: x.importance, reverse=True)
                
                # Base value (expected value)
                base_value = float(self.explainer.expected_value)
                
                return ShapExplanation(
                    features=shap_features,
                    base_value=base_value,
                    prediction=risk_score
                )
                
            except Exception as e:
                print(f"⚠️  Error in SHAP explanation: {e}")
                print("⚠️  Falling back to mock SHAP values")
                # Fallback to mock
                pass
        
        # Mock SHAP values (fallback)
        shap_dict = self._mock_shap_values(features, risk_score)
        
        shap_features = []
        for feature_name, importance in shap_dict.items():
            shap_features.append(ShapFeature(
                feature_name=feature_name,
                importance=abs(importance),
                direction='positive' if importance > 0 else 'negative',
                display_name_tr=self.FEATURE_NAMES_TR.get(feature_name, feature_name)
            ))
        
        shap_features.sort(key=lambda x: x.importance, reverse=True)
        
        return ShapExplanation(
            features=shap_features,
            base_value=0.3,
            prediction=risk_score
        )
    
    def get_top_features(self, shap_values: List[ShapFeature], n: int = 5) -> List[ShapFeature]:
        """
        Extract top N features by absolute importance
        """
        return shap_values[:n]
    
    def get_natural_language_explanation(self, shap_features: List[ShapFeature]) -> str:
        """
        Generate natural language explanation in Turkish for Iranian model
        """
        if not shap_features:
            return "Risk faktörü bulunamadı."
        
        top_features = shap_features[:3]
        
        explanations = []
        for feature in top_features:
            if feature.direction == 'positive':
                if 'call_failure' in feature.feature_name.lower():
                    explanations.append("Başarısız arama deneyimleri yaşamış")
                elif 'complaint' in feature.feature_name.lower():
                    explanations.append("Çağrı merkezini arayıp şikayette bulunmuş")
                elif 'tenure' in feature.feature_name.lower():
                    explanations.append("Yeni abone (rakip tekliflere açık)")
                elif 'charge' in feature.feature_name.lower():
                    explanations.append("Faturasında ani bir artış yaşanmış")
                elif 'seconds' in feature.feature_name.lower():
                    explanations.append("Hizmeti aktif kullanmıyor")
                elif 'frequency' in feature.feature_name.lower():
                    explanations.append("Düşük kullanım sıklığı")
                elif 'sms' in feature.feature_name.lower():
                    explanations.append("SMS kullanımı düşük")
                elif 'distinct' in feature.feature_name.lower() or 'called' in feature.feature_name.lower():
                    explanations.append("Sınırlı iletişim çevresi")
                elif 'age' in feature.feature_name.lower():
                    explanations.append("Genç yaş grubu (daha hareketli)")
                elif 'tariff' in feature.feature_name.lower():
                    explanations.append("Tarife planı uyumsuzluğu")
            else:
                if 'tenure' in feature.feature_name.lower():
                    explanations.append("Uzun yıllardır müşteri (sadık profil)")
                elif 'seconds' in feature.feature_name.lower():
                    explanations.append("Hizmeti yoğun kullanıyor")
                elif 'frequency' in feature.feature_name.lower():
                    explanations.append("Yüksek kullanım sıklığı")
                elif 'sms' in feature.feature_name.lower():
                    explanations.append("Aktif SMS kullanıcısı")
                elif 'distinct' in feature.feature_name.lower() or 'called' in feature.feature_name.lower():
                    explanations.append("Geniş iletişim çevresi")
                elif 'age' in feature.feature_name.lower():
                    explanations.append("Olgun yaş grubu (daha istikrarlı)")
                elif 'call_failure' in feature.feature_name.lower():
                    explanations.append("Kaliteli bağlantı deneyimi")
                elif 'tariff' in feature.feature_name.lower():
                    explanations.append("Uygun tarife planı")
        
        if explanations:
            return "Ana faktörler: " + ", ".join(explanations) + "."
        else:
            return "Risk faktörleri analiz edildi."
