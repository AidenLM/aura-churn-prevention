# Frontend Güncelleme Rehberi - TrustedModel

## Özet
Backend TrustedModel'e geçirildi. Frontend'in güncellenmesi gereken kısımlar:

## 1. API Types Güncellendi ✅
**Dosya**: `aura-frontend/lib/api.ts`

### Değişiklikler:
- `RiskCalculationInput`: 10 feature → 19 TrustedModel feature
- `CustomerDetail`: email/phone nullable oldu (dataset'te yok)
- Mock data güncellendi (7043 müşteri)

### Yeni Feature'lar (19):
```typescript
// Demographic (4)
gender: string;  // Male, Female
senior_citizen: number;  // 0 or 1
partner: string;  // Yes, No
dependents: string;  // Yes, No

// Account (5)
tenure: number;  // months
contract: string;  // Month-to-month, One year, Two year
paperless_billing: string;  // Yes, No
payment_method: string;  // Electronic check, Mailed check, Bank transfer, Credit card
monthly_charges: number;
total_charges: number;

// Phone Services (2)
phone_service: string;  // Yes, No
multiple_lines: string;  // Yes, No, No phone service

// Internet Services (7)
internet_service: string;  // DSL, Fiber optic, No
online_security: string;  // Yes, No, No internet service
online_backup: string;  // Yes, No, No internet service
device_protection: string;  // Yes, No, No internet service
tech_support: string;  // Yes, No, No internet service
streaming_tv: string;  // Yes, No, No internet service
streaming_movies: string;  // Yes, No, No internet service
```

## 2. Calculator Page Güncellenmeli ❌
**Dosya**: `aura-frontend/app/calculator/page.tsx`

### Yapılacaklar:
1. Form state'i 19 feature'a güncellenmeli
2. Form UI 4 bölüme ayrılmalı:
   - Demografik Bilgiler (4 field)
   - Hesap Bilgileri (5 field)
   - Telefon Hizmetleri (2 field)
   - İnternet Hizmetleri (7 field)
3. Her field için uygun input tipi:
   - Select dropdown'lar (Yes/No, contract types, etc.)
   - Number input'lar (tenure, charges)
4. Türkçe label'lar

### Örnek Form Yapısı:
```tsx
const [formData, setFormData] = useState<RiskCalculationInput>({
  // Demographic
  gender: 'Male',
  senior_citizen: 0,
  partner: 'No',
  dependents: 'No',
  // Account
  tenure: 12,
  contract: 'Month-to-month',
  paperless_billing: 'Yes',
  payment_method: 'Electronic check',
  monthly_charges: 70.0,
  total_charges: 840.0,
  // Phone
  phone_service: 'Yes',
  multiple_lines: 'No',
  // Internet
  internet_service: 'Fiber optic',
  online_security: 'No',
  online_backup: 'No',
  device_protection: 'No',
  tech_support: 'No',
  streaming_tv: 'No',
  streaming_movies: 'No',
});
```

## 3. Customer Detail Page Güncellenmeli ❌
**Dosya**: `aura-frontend/app/customers/[id]/page.tsx`

### Yapılacaklar:
1. Email/Phone null check ekle (dataset'te yok)
2. Plan type → internet_service mapping
3. Kullanılmayan field'ları gizle veya kaldır:
   - complaint_count (0)
   - support_calls_count (0)
   - payment_delays (0)
   - data_usage_gb (0)
   - voice_minutes (0)
4. TrustedModel feature'larını göster:
   - Gender, Senior Citizen, Partner, Dependents
   - Contract type, Paperless billing, Payment method
   - Phone service, Multiple lines
   - Internet services (7 feature)

## 4. Dashboard Page - Çalışıyor ✅
**Dosya**: `aura-frontend/app/dashboard/page.tsx`

Dashboard API'si çalışıyor, değişiklik gerekmez.

## 5. Customers List Page Güncellenmeli ❌
**Dosya**: `aura-frontend/app/customers/page.tsx`

### Yapılacaklar:
1. Email kolonu nullable olmalı
2. Plan type → internet_service

## 6. Türkçe Label Mapping

### Feature İsimleri:
```typescript
const featureLabels = {
  // Demographic
  gender: 'Cinsiyet',
  senior_citizen: 'Yaşlı Vatandaş',
  partner: 'Eş Durumu',
  dependents: 'Bakmakla Yükümlü',
  
  // Account
  tenure: 'Müşteri Süresi (ay)',
  contract: 'Sözleşme Tipi',
  paperless_billing: 'Kağıtsız Fatura',
  payment_method: 'Ödeme Yöntemi',
  monthly_charges: 'Aylık Ücret',
  total_charges: 'Toplam Ücret',
  
  // Phone
  phone_service: 'Telefon Hizmeti',
  multiple_lines: 'Çoklu Hat',
  
  // Internet
  internet_service: 'İnternet Hizmeti',
  online_security: 'Online Güvenlik',
  online_backup: 'Online Yedekleme',
  device_protection: 'Cihaz Koruma',
  tech_support: 'Teknik Destek',
  streaming_tv: 'TV Yayını',
  streaming_movies: 'Film Yayını',
};
```

### Değer Çevirileri:
```typescript
const valueTranslations = {
  // Yes/No
  'Yes': 'Evet',
  'No': 'Hayır',
  
  // Gender
  'Male': 'Erkek',
  'Female': 'Kadın',
  
  // Contract
  'Month-to-month': 'Aylık',
  'One year': '1 Yıl',
  'Two year': '2 Yıl',
  
  // Payment Method
  'Electronic check': 'Elektronik Çek',
  'Mailed check': 'Posta Çeki',
  'Bank transfer (automatic)': 'Otomatik Banka Transferi',
  'Credit card (automatic)': 'Otomatik Kredi Kartı',
  
  // Internet Service
  'DSL': 'DSL',
  'Fiber optic': 'Fiber Optik',
  
  // Service Status
  'No phone service': 'Telefon Hizmeti Yok',
  'No internet service': 'İnternet Hizmeti Yok',
};
```

## 7. Test Senaryoları

### Backend Test (Çalışıyor ✅):
```bash
cd aura-backend
python test_api_integration.py
```

### Frontend Test (Yapılacak):
1. Calculator sayfasını aç
2. Tüm 19 field'ı doldur
3. "Risk Hesapla" butonuna tıkla
4. Sonuç görüntülenmeli (risk score, level, AI analysis)

### API Test:
```bash
# Dashboard
curl http://localhost:8000/api/dashboard/summary

# Random Customer
curl http://localhost:8000/api/customers/random/get

# Risk Calculation
curl -X POST http://localhost:8000/api/predict/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "senior_citizen": 0,
    "partner": "Yes",
    "dependents": "No",
    "tenure": 12,
    "contract": "Month-to-month",
    "paperless_billing": "Yes",
    "payment_method": "Electronic check",
    "monthly_charges": 85.0,
    "total_charges": 1020.0,
    "phone_service": "Yes",
    "multiple_lines": "No",
    "internet_service": "Fiber optic",
    "online_security": "No",
    "online_backup": "No",
    "device_protection": "No",
    "tech_support": "No",
    "streaming_tv": "Yes",
    "streaming_movies": "Yes"
  }'
```

## 8. Deployment Checklist

### Backend ✅:
- [x] Model trained (Voting Classifier, 79.98% accuracy)
- [x] Database migrated (7,043 customers)
- [x] API endpoints updated
- [x] Integration tests passing

### Frontend ❌:
- [x] API types updated
- [ ] Calculator page updated
- [ ] Customer detail page updated
- [ ] Customer list page updated
- [ ] Turkish translations added
- [ ] End-to-end testing

## 9. Sonraki Adımlar

1. **Calculator Page**: 19 feature form oluştur
2. **Customer Pages**: TrustedModel field'larını göster
3. **Testing**: End-to-end test
4. **SHAP Explainer**: Backend'de implement et (TODO)
5. **Offer Optimizer**: Backend'de implement et veya kaldır (TODO)

---
**Tarih**: 15 Şubat 2026
**Status**: Backend Complete ✅, Frontend Pending ❌
