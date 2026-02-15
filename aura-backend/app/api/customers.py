"""Customer API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.db.base import get_db
from app.repositories.customer_repository import CustomerRepository
from app.services.churn_predictor import ChurnPredictor

router = APIRouter(prefix="/api/customers", tags=["customers"])

# Initialize services
predictor = ChurnPredictor()


def _generate_shap_values(customer, prediction: dict) -> list:
    """
    Generate SHAP-like feature importance values for TrustedModel
    
    Analyzes all 19 features used in the ML model:
    1. Gender, 2. SeniorCitizen, 3. Partner, 4. Dependents, 5. Tenure
    6. PhoneService, 7. MultipleLines, 8. InternetService, 9. OnlineSecurity
    10. OnlineBackup, 11. DeviceProtection, 12. TechSupport, 13. StreamingTV
    14. StreamingMovies, 15. Contract, 16. PaperlessBilling, 17. PaymentMethod
    18. MonthlyCharges, 19. TotalCharges
    
    Returns top features that contribute to churn risk
    """
    shap_features = []
    risk_score = prediction['churn_probability']
    monthly = float(customer.monthly_charges)
    total = float(customer.total_charges)
    
    # 1. Tenure analysis (HIGH IMPORTANCE)
    if customer.tenure < 6:
        shap_features.append({
            "feature_name": "tenure",
            "importance": 0.18,
            "direction": "positive",
            "display_name_tr": "Müşteri Süresi"
        })
    elif customer.tenure < 12:
        shap_features.append({
            "feature_name": "tenure",
            "importance": 0.12,
            "direction": "positive",
            "display_name_tr": "Müşteri Süresi"
        })
    elif customer.tenure > 48:
        shap_features.append({
            "feature_name": "tenure",
            "importance": 0.15,
            "direction": "negative",
            "display_name_tr": "Müşteri Süresi"
        })
    
    # 2. Contract type (HIGH IMPORTANCE)
    if customer.contract == "Month-to-month":
        shap_features.append({
            "feature_name": "contract",
            "importance": 0.20,
            "direction": "positive",
            "display_name_tr": "Sözleşme Tipi"
        })
    elif customer.contract == "One year":
        shap_features.append({
            "feature_name": "contract",
            "importance": 0.10,
            "direction": "negative",
            "display_name_tr": "Sözleşme Tipi"
        })
    elif customer.contract == "Two year":
        shap_features.append({
            "feature_name": "contract",
            "importance": 0.16,
            "direction": "negative",
            "display_name_tr": "Sözleşme Tipi"
        })
    
    # 3. Monthly charges (HIGH IMPORTANCE)
    if monthly > 80:
        shap_features.append({
            "feature_name": "monthly_charges",
            "importance": 0.14,
            "direction": "positive",
            "display_name_tr": "Aylık Ücret"
        })
    elif monthly > 60:
        shap_features.append({
            "feature_name": "monthly_charges",
            "importance": 0.09,
            "direction": "positive",
            "display_name_tr": "Aylık Ücret"
        })
    elif monthly < 30:
        shap_features.append({
            "feature_name": "monthly_charges",
            "importance": 0.08,
            "direction": "negative",
            "display_name_tr": "Aylık Ücret"
        })
    
    # 4. Total charges
    if total < 500 and customer.tenure > 6:
        shap_features.append({
            "feature_name": "total_charges",
            "importance": 0.07,
            "direction": "positive",
            "display_name_tr": "Toplam Ücret"
        })
    elif total > 5000:
        shap_features.append({
            "feature_name": "total_charges",
            "importance": 0.09,
            "direction": "negative",
            "display_name_tr": "Toplam Ücret"
        })
    
    # 5. Payment method (MEDIUM IMPORTANCE)
    if customer.payment_method == "Electronic check":
        shap_features.append({
            "feature_name": "payment_method",
            "importance": 0.13,
            "direction": "positive",
            "display_name_tr": "Ödeme Yöntemi"
        })
    elif customer.payment_method in ["Bank transfer (automatic)", "Credit card (automatic)"]:
        shap_features.append({
            "feature_name": "payment_method",
            "importance": 0.10,
            "direction": "negative",
            "display_name_tr": "Ödeme Yöntemi"
        })
    
    # 6. Internet service (MEDIUM IMPORTANCE)
    if customer.internet_service == "Fiber optic":
        shap_features.append({
            "feature_name": "internet_service",
            "importance": 0.11,
            "direction": "positive",
            "display_name_tr": "İnternet Hizmeti"
        })
    elif customer.internet_service == "DSL":
        shap_features.append({
            "feature_name": "internet_service",
            "importance": 0.05,
            "direction": "negative",
            "display_name_tr": "İnternet Hizmeti"
        })
    elif customer.internet_service == "No":
        shap_features.append({
            "feature_name": "internet_service",
            "importance": 0.08,
            "direction": "negative",
            "display_name_tr": "İnternet Hizmeti"
        })
    
    # 7. Tech support (MEDIUM IMPORTANCE)
    if customer.tech_support == "No" and customer.internet_service != "No":
        shap_features.append({
            "feature_name": "tech_support",
            "importance": 0.10,
            "direction": "positive",
            "display_name_tr": "Teknik Destek"
        })
    elif customer.tech_support == "Yes":
        shap_features.append({
            "feature_name": "tech_support",
            "importance": 0.09,
            "direction": "negative",
            "display_name_tr": "Teknik Destek"
        })
    
    # 8. Online security (MEDIUM IMPORTANCE)
    if customer.online_security == "No" and customer.internet_service != "No":
        shap_features.append({
            "feature_name": "online_security",
            "importance": 0.09,
            "direction": "positive",
            "display_name_tr": "Çevrimiçi Güvenlik"
        })
    elif customer.online_security == "Yes":
        shap_features.append({
            "feature_name": "online_security",
            "importance": 0.08,
            "direction": "negative",
            "display_name_tr": "Çevrimiçi Güvenlik"
        })
    
    # 9. Online backup
    if customer.online_backup == "No" and customer.internet_service != "No":
        shap_features.append({
            "feature_name": "online_backup",
            "importance": 0.07,
            "direction": "positive",
            "display_name_tr": "Çevrimiçi Yedekleme"
        })
    elif customer.online_backup == "Yes":
        shap_features.append({
            "feature_name": "online_backup",
            "importance": 0.06,
            "direction": "negative",
            "display_name_tr": "Çevrimiçi Yedekleme"
        })
    
    # 10. Device protection
    if customer.device_protection == "No" and customer.internet_service != "No":
        shap_features.append({
            "feature_name": "device_protection",
            "importance": 0.06,
            "direction": "positive",
            "display_name_tr": "Cihaz Koruma"
        })
    elif customer.device_protection == "Yes":
        shap_features.append({
            "feature_name": "device_protection",
            "importance": 0.05,
            "direction": "negative",
            "display_name_tr": "Cihaz Koruma"
        })
    
    # 11. Streaming TV
    if customer.streaming_tv == "Yes":
        shap_features.append({
            "feature_name": "streaming_tv",
            "importance": 0.04,
            "direction": "positive",
            "display_name_tr": "Streaming TV"
        })
    
    # 12. Streaming Movies
    if customer.streaming_movies == "Yes":
        shap_features.append({
            "feature_name": "streaming_movies",
            "importance": 0.04,
            "direction": "positive",
            "display_name_tr": "Streaming Film"
        })
    
    # 13. Paperless billing
    if customer.paperless_billing == "Yes":
        shap_features.append({
            "feature_name": "paperless_billing",
            "importance": 0.06,
            "direction": "positive",
            "display_name_tr": "Kağıtsız Fatura"
        })
    
    # 14. Partner and dependents (FAMILY STATUS)
    if customer.partner == "No" and customer.dependents == "No":
        shap_features.append({
            "feature_name": "family_status",
            "importance": 0.08,
            "direction": "positive",
            "display_name_tr": "Aile Durumu"
        })
    elif customer.partner == "Yes" and customer.dependents == "Yes":
        shap_features.append({
            "feature_name": "family_status",
            "importance": 0.07,
            "direction": "negative",
            "display_name_tr": "Aile Durumu"
        })
    elif customer.partner == "Yes":
        shap_features.append({
            "feature_name": "partner",
            "importance": 0.05,
            "direction": "negative",
            "display_name_tr": "Partner"
        })
    
    # 15. Senior citizen
    if customer.senior_citizen == 1:
        shap_features.append({
            "feature_name": "senior_citizen",
            "importance": 0.05,
            "direction": "positive",
            "display_name_tr": "Yaşlı Vatandaş"
        })
    
    # 16. Phone service
    if customer.phone_service == "Yes":
        shap_features.append({
            "feature_name": "phone_service",
            "importance": 0.03,
            "direction": "negative",
            "display_name_tr": "Telefon Hizmeti"
        })
    
    # 17. Multiple lines
    if customer.multiple_lines == "Yes":
        shap_features.append({
            "feature_name": "multiple_lines",
            "importance": 0.04,
            "direction": "positive",
            "display_name_tr": "Çoklu Hat"
        })
    
    # 18. Gender (LOW IMPORTANCE)
    if customer.gender == "Female":
        shap_features.append({
            "feature_name": "gender",
            "importance": 0.02,
            "direction": "positive",
            "display_name_tr": "Cinsiyet"
        })
    
    # Sort by importance
    shap_features.sort(key=lambda x: x["importance"], reverse=True)
    
    # Return top 8 (increased from 5 to show more features)
    return shap_features[:8]


def _generate_detailed_insights(customer, prediction: dict) -> str:
    """
    Generate detailed AI insights in Turkish for customer churn analysis
    Returns structured insights with clear sections
    """
    risk_level = prediction['risk_level']
    risk_prob = prediction['churn_probability'] * 100
    
    insights = []
    
    # 1. Risk Assessment (concise)
    if risk_level == "High":
        insights.append(f"Bu müşteri YÜKSEK risk grubunda (%{risk_prob:.1f} kayıp olasılığı). Acil müdahale gerekiyor.")
    elif risk_level == "Medium":
        insights.append(f"Bu müşteri ORTA risk grubunda (%{risk_prob:.1f} kayıp olasılığı). Yakından takip edilmeli.")
    else:
        insights.append(f"Bu müşteri DÜŞÜK risk grubunda (%{risk_prob:.1f} kayıp olasılığı). Sadık müşteri profili.")
    
    # 2. Key Factors (2-3 most important)
    factors = []
    tenure = customer.tenure
    contract = customer.contract
    monthly = float(customer.monthly_charges)
    payment = customer.payment_method
    
    if tenure < 6:
        factors.append(f"Yeni müşteri ({tenure} ay)")
    elif tenure > 36:
        factors.append(f"Uzun süreli müşteri ({tenure} ay)")
    
    if contract == "Month-to-month":
        factors.append("Aylık sözleşme (yüksek esneklik)")
    elif contract == "Two year":
        factors.append("2 yıllık sözleşme (yüksek bağlılık)")
    
    if monthly > 80:
        factors.append(f"Yüksek ücret ({monthly:.0f} TL)")
    
    if payment == "Electronic check":
        factors.append("Manuel ödeme yöntemi")
    
    if factors:
        insights.append("Ana faktörler: " + ", ".join(factors[:3]) + ".")
    
    # 3. Recommended Actions (based on risk)
    if risk_level == "High":
        insights.append("ACİL|48 saat içinde iletişim|KAMPANYA|Özel indirim paketi|DESTEK|Hesap yöneticisi ataması")
    elif risk_level == "Medium":
        insights.append("İLETİŞİM|1 hafta içinde görüşme|SADAKAT|Sadakat programına dahil et|ANALİZ|Kullanım paternlerini incele")
    else:
        insights.append("ANKET|Memnuniyet anketi|VIP|VIP statü değerlendir|REFERANS|Referans programına dahil et")
    
    return "|||".join(insights)  # Use ||| as section separator


class ShapFeature(BaseModel):
    """SHAP feature importance"""
    feature_name: str
    importance: float
    direction: str
    display_name_tr: str


class PlanInfo(BaseModel):
    """Customer plan information"""
    type: str
    monthly_charge: float


class OfferRecommendation(BaseModel):
    """Offer recommendation"""
    campaign_name: str
    discount_percentage: int
    duration_months: int
    estimated_cost: float
    rationale: str


class CustomerDetailResponse(BaseModel):
    """Customer detail response"""
    customer_id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    risk_score: float
    risk_level: str
    plan_type: str
    monthly_charge: float
    tenure: int
    ai_insights: str
    shap_values: List[ShapFeature]
    recommended_offer: Optional[OfferRecommendation]
    # Actual customer metrics for context
    complaint_count: int
    support_calls_count: int
    payment_delays: int
    data_usage_gb: float
    voice_minutes: int
    contract_type: str


class HighRiskCustomersResponse(BaseModel):
    """High-risk customers list response"""
    customers: List[dict]
    total: int


class AllCustomersResponse(BaseModel):
    """All customers list response"""
    customers: List[dict]
    total: int
    page: int
    page_size: int


@router.get("/{customer_id}", response_model=CustomerDetailResponse)
async def get_customer_detail(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed customer information with risk analysis
    
    Args:
        customer_id: Customer ID
        
    Returns:
        Complete customer profile with risk prediction, SHAP analysis,
        AI insights, and offer recommendation
    """
    try:
        repo = CustomerRepository(db)
        
        # Get customer
        customer = repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f"Müşteri bulunamadı: {customer_id}"
            )
        
        # Prepare customer data for prediction
        customer_data = {
            "customer_id": customer.customer_id,
            "gender": customer.gender,
            "senior_citizen": customer.senior_citizen,
            "partner": customer.partner,
            "dependents": customer.dependents,
            "tenure": customer.tenure,
            "contract": customer.contract,
            "paperless_billing": customer.paperless_billing,
            "payment_method": customer.payment_method,
            "monthly_charges": float(customer.monthly_charges),
            "total_charges": float(customer.total_charges),
            "phone_service": customer.phone_service,
            "multiple_lines": customer.multiple_lines,
            "internet_service": customer.internet_service,
            "online_security": customer.online_security,
            "online_backup": customer.online_backup,
            "device_protection": customer.device_protection,
            "tech_support": customer.tech_support,
            "streaming_tv": customer.streaming_tv,
            "streaming_movies": customer.streaming_movies
        }
        
        # Get prediction
        prediction = predictor.predict(customer_data)
        
        # Generate detailed AI insights in Turkish
        ai_insights = _generate_detailed_insights(customer, prediction)
        
        # Generate SHAP values
        shap_features_list = _generate_shap_values(customer, prediction)
        
        # Add top SHAP features to AI insights
        if shap_features_list:
            top_shap_features = [f"{f['display_name_tr']} ({'artırıyor' if f['direction'] == 'positive' else 'azaltıyor'})" 
                                for f in shap_features_list[:3]]
            shap_summary = "ML Model Faktörleri: " + ", ".join(top_shap_features) + "."
            # Insert SHAP summary as second section
            sections = ai_insights.split('|||')
            if len(sections) >= 2:
                ai_insights = sections[0] + '|||' + shap_summary + '|||' + '|||'.join(sections[1:])
            else:
                ai_insights = ai_insights + '|||' + shap_summary
        
        # TODO: Implement SHAP explainer for TrustedModel
        # TODO: Implement offer optimizer for TrustedModel
        
        # Save prediction to audit trail
        repo.save_prediction(
            customer_id=customer.customer_id,
            risk_score=prediction["churn_probability"],
            risk_level=prediction["risk_level"],
            shap_values={}  # TODO: Add SHAP values when implemented
        )
        
        return CustomerDetailResponse(
            customer_id=customer.customer_id,
            name=customer.customer_id,  # Using customer_id as name for now
            email=None,  # Not in TrustedModel dataset
            phone=None,  # Not in TrustedModel dataset
            risk_score=prediction["churn_probability"],
            risk_level=prediction["risk_level"],
            plan_type=customer.internet_service,  # Using internet service as plan type
            monthly_charge=float(customer.monthly_charges),
            tenure=customer.tenure,
            ai_insights=ai_insights,
            shap_values=shap_features_list,
            recommended_offer=None,  # TODO: Implement offers
            complaint_count=0,  # Not in TrustedModel dataset
            support_calls_count=0,  # Not in TrustedModel dataset
            payment_delays=0,  # Not in TrustedModel dataset
            data_usage_gb=0.0,  # Not in TrustedModel dataset
            voice_minutes=0,  # Not in TrustedModel dataset
            contract_type=customer.contract
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Müşteri verisi alınırken hata oluştu: {str(e)}"
        )


@router.get("/high-risk/list", response_model=HighRiskCustomersResponse)
async def get_high_risk_customers(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get list of high-risk customers
    
    Args:
        limit: Maximum number of customers to return (1-100)
        
    Returns:
        List of high-risk customers with basic info
    """
    try:
        repo = CustomerRepository(db)
        
        # Get high-risk customers
        customers = repo.get_high_risk_customers(limit=limit)
        
        # Build response
        customer_list = []
        for customer in customers:
            prediction = repo.get_latest_prediction(customer.customer_id)
            if prediction:
                customer_list.append({
                    "customer_id": customer.customer_id,
                    "name": customer.customer_id,  # Using customer_id as name
                    "risk_score": float(prediction.risk_score),
                    "risk_level": prediction.risk_level,
                    "plan_type": customer.internet_service,
                    "monthly_charge": float(customer.monthly_charges)
                })
        
        return HighRiskCustomersResponse(
            customers=customer_list,
            total=len(customer_list)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Yüksek riskli müşteriler alınırken hata oluştu: {str(e)}"
        )


@router.get("/random/get")
async def get_random_customer(db: Session = Depends(get_db)):
    """
    Get a random customer for demo purposes
    
    Returns:
        Random customer detail (same format as get_customer_detail)
    """
    try:
        repo = CustomerRepository(db)
        
        # Get random customer
        customer = repo.get_random_customer()
        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Veritabanında müşteri bulunamadı"
            )
        
        # Return customer detail
        return await get_customer_detail(customer.customer_id, db)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Rastgele müşteri alınırken hata oluştu: {str(e)}"
        )


@router.get("/all/list", response_model=AllCustomersResponse)
async def get_all_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all customers with pagination
    
    Args:
        page: Page number (starts from 1)
        page_size: Number of customers per page (1-100)
        
    Returns:
        Paginated list of all customers
    """
    try:
        from app.db.models import Customer, PredictionRecord
        offset = (page - 1) * page_size
        
        customers_query = db.query(Customer).offset(offset).limit(page_size).all()
        total_count = db.query(Customer).count()
        
        # Build response
        customer_list = []
        for customer in customers_query:
            # Get latest prediction
            prediction = db.query(PredictionRecord).filter(
                PredictionRecord.customer_id == customer.customer_id
            ).order_by(PredictionRecord.timestamp.desc()).first()
            
            risk_score = float(prediction.risk_score) if prediction else 0.0
            risk_level = prediction.risk_level if prediction else "Unknown"
            
            customer_list.append({
                "customer_id": customer.customer_id,
                "name": customer.customer_id,  # Using customer_id as name
                "email": None,  # Not in TrustedModel
                "plan_type": customer.internet_service,
                "monthly_charge": float(customer.monthly_charges),
                "tenure": customer.tenure,
                "risk_score": risk_score,
                "risk_level": risk_level
            })
        
        return AllCustomersResponse(
            customers=customer_list,
            total=total_count,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Müşteriler alınırken hata oluştu: {str(e)}"
        )
