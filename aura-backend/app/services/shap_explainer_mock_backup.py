import numpy as np
from typing import List
from app.schemas.customer import CustomerFeatures, ShapFeature, ShapExplanation

class ShapExplainer:
    """
    SHAP explainability service for churn predictions
    
    This service generates feature importance explanations using SHAP values
    to help understand why a customer is predicted to churn.
    """
    
    # Turkish feature name mappings
    FEATURE_NAMES_TR = {
        'tenure': 'Üyelik Süresi',
        'plan_type': 'Tarife Planı',
        'monthly_charge': 'Aylık Fatura',
        'data_usage_gb': 'Veri Kullanımı',
        'voice_minutes': 'Arama Süresi',
        'sms_count': 'SMS Sayısı',
        'complaint_count': 'Şikayet Sayısı',
        'support_calls_count': 'Destek Çağrısı',
        'payment_delays': 'Ödeme Gecikmeleri',
        'contract_type': 'Sözleşme Tipi'
    }
    
    def __init__(self, model=None, background_data=None):
        """
        Initialize SHAP explainer
        
        Args:
            model: XGBoost model (optional for now)
            background_data: Background dataset for SHAP (optional)
        """
        self.model = model
        self.background_data = background_data
        self.explainer = None
        
        # In production, this would initialize:
        # self.explainer = shap.TreeExplainer(model, background_data)
    
    def _mock_shap_values(self, features: CustomerFeatures, risk_score: float) -> dict:
        """
        Generate mock SHAP values (until real model is trained)
        
        This creates realistic SHAP values based on customer features.
        Positive values increase risk, negative values decrease risk.
        
        Args:
            features: CustomerFeatures object
            risk_score: Predicted risk score
            
        Returns:
            Dictionary of feature names to SHAP values
        """
        shap_values = {}
        
        # Complaint count (high complaints = high positive SHAP)
        if features.complaint_count > 0:
            shap_values['complaint_count'] = features.complaint_count * 0.08
        
        # Payment delays (delays = high positive SHAP)
        if features.payment_delays > 0:
            shap_values['payment_delays'] = features.payment_delays * 0.12
        
        # Tenure (low tenure = positive SHAP, high tenure = negative SHAP)
        if features.tenure < 6:
            shap_values['tenure'] = 0.15
        elif features.tenure > 24:
            shap_values['tenure'] = -0.12
        
        # Data usage (low usage = positive SHAP)
        if features.data_usage_gb < 5:
            shap_values['data_usage_gb'] = 0.10
        elif features.data_usage_gb > 20:
            shap_values['data_usage_gb'] = -0.08
        
        # Monthly charge (high charge with low usage = positive SHAP)
        if features.monthly_charge > 200 and features.data_usage_gb < 10:
            shap_values['monthly_charge'] = 0.15
        elif features.monthly_charge < 100:
            shap_values['monthly_charge'] = -0.05
        
        # Support calls
        if features.support_calls_count > 3:
            shap_values['support_calls_count'] = features.support_calls_count * 0.03
        
        # Contract type (annual = negative SHAP)
        if features.contract_type == 'Annual':
            shap_values['contract_type'] = -0.10
        else:
            shap_values['contract_type'] = 0.05
        
        # Voice minutes (low usage = positive SHAP)
        if features.voice_minutes < 100:
            shap_values['voice_minutes'] = 0.05
        elif features.voice_minutes > 500:
            shap_values['voice_minutes'] = -0.06
        
        return shap_values
    
    def explain(self, features: CustomerFeatures, risk_score: float) -> ShapExplanation:
        """
        Generate SHAP values for customer features
        
        Args:
            features: CustomerFeatures to explain
            risk_score: Predicted risk score
            
        Returns:
            ShapExplanation with feature importances and base value
        """
        # Get SHAP values (mock for now)
        if self.explainer is None:
            shap_dict = self._mock_shap_values(features, risk_score)
        else:
            # Real SHAP explanation
            # shap_values = self.explainer.shap_values(features_array)
            pass
        
        # Convert to ShapFeature objects
        shap_features = []
        for feature_name, importance in shap_dict.items():
            shap_features.append(ShapFeature(
                feature_name=feature_name,
                importance=abs(importance),
                direction='positive' if importance > 0 else 'negative',
                display_name_tr=self.FEATURE_NAMES_TR.get(feature_name, feature_name)
            ))
        
        # Sort by absolute importance
        shap_features.sort(key=lambda x: x.importance, reverse=True)
        
        # Base value (average prediction)
        base_value = 0.3
        
        return ShapExplanation(
            features=shap_features,
            base_value=base_value,
            prediction=risk_score
        )
    
    def get_top_features(self, shap_values: List[ShapFeature], n: int = 5) -> List[ShapFeature]:
        """
        Extract top N features by absolute importance
        
        Args:
            shap_values: List of ShapFeature objects
            n: Number of top features to return
            
        Returns:
            List of top N ShapFeature objects
        """
        # Already sorted by importance in explain()
        return shap_values[:n]
    
    def get_natural_language_explanation(self, shap_features: List[ShapFeature]) -> str:
        """
        Generate natural language explanation in Turkish
        
        Args:
            shap_features: List of ShapFeature objects
            
        Returns:
            Turkish explanation string
        """
        if not shap_features:
            return "Risk faktörü bulunamadı."
        
        # Get top 3 features
        top_features = shap_features[:3]
        
        explanations = []
        for feature in top_features:
            if feature.direction == 'positive':
                # Risk-increasing factors
                if feature.feature_name == 'complaint_count':
                    explanations.append("Çağrı merkezini arayıp şikayette bulunmuş")
                elif feature.feature_name == 'payment_delays':
                    explanations.append("Ödemelerinde gecikmeler var")
                elif feature.feature_name == 'tenure':
                    explanations.append("Yeni abone (rakip tekliflere açık)")
                elif feature.feature_name == 'data_usage_gb':
                    explanations.append("Hizmeti aktif kullanmıyor")
                elif feature.feature_name == 'monthly_charge':
                    explanations.append("Faturasında ani bir artış yaşanmış")
                elif feature.feature_name == 'support_calls_count':
                    explanations.append("Sık sık destek hattını arıyor")
                elif feature.feature_name == 'contract_type':
                    explanations.append("Taahhütsüz kullanıyor")
                elif feature.feature_name == 'voice_minutes':
                    explanations.append("Arama yapmıyor (düşük kullanım)")
            else:
                # Risk-decreasing factors
                if feature.feature_name == 'tenure':
                    explanations.append("Uzun yıllardır müşteri (sadık profil)")
                elif feature.feature_name == 'contract_type':
                    explanations.append("Taahhütlü sözleşmesi var")
                elif feature.feature_name == 'data_usage_gb':
                    explanations.append("Hizmeti yoğun kullanıyor")
                elif feature.feature_name == 'monthly_charge':
                    explanations.append("Fatura tutarı düzenli")
                elif feature.feature_name == 'voice_minutes':
                    explanations.append("Aktif olarak arama yapıyor")
        
        if explanations:
            return "Ana faktörler: " + ", ".join(explanations) + "."
        else:
            return "Risk faktörleri analiz edildi."
