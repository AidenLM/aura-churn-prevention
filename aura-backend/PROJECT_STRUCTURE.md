# AURA Projesi - Tam Klasör Yapısı

## 📁 Proje Kök Dizini

```
aura-project/
├── aura-frontend/          # Next.js 15 Frontend
├── aura-backend/           # FastAPI Backend
├── .kiro/                  # Spec dosyaları
└── README.md
```

---

## 🎨 Frontend Yapısı (aura-frontend/)

```
aura-frontend/
├── app/                                    # Next.js 15 App Router
│   ├── page.tsx                           # Ana sayfa (Landing - DARK THEME)
│   ├── layout.tsx                         # Root layout
│   ├── globals.css                        # Global CSS
│   ├── favicon.ico
│   │
│   ├── dashboard/                         # Dashboard sayfası
│   │   ├── page.tsx                       # Dashboard ana sayfa
│   │   ├── loading.tsx                    # Loading skeleton
│   │   └── components/                    # Dashboard bileşenleri
│   │       ├── ResponsiveDashboard.tsx
│   │       ├── RiskDistributionChart.tsx  # Recharts bar chart
│   │       └── TopRiskyCustomersChart.tsx # Recharts horizontal bar
│   │
│   ├── customers/                         # Müşteri sayfaları
│   │   ├── page.tsx                       # Müşteri listesi (250 müşteri)
│   │   ├── [id]/                          # Dinamik müşteri detay
│   │   │   ├── page.tsx                   # Müşteri detay sayfası
│   │   │   └── loading.tsx                # Loading skeleton
│   │   └── components/
│   │       └── ShapChart.tsx              # SHAP feature importance chart
│   │
│   ├── calculator/                        # Risk hesaplama
│   │   ├── page.tsx                       # Risk calculator form
│   │   └── loading.tsx                    # Loading skeleton
│   │
│   ├── simulation/                        # ROI simülasyonu
│   │   ├── page.tsx                       # Kampanya simülasyonu
│   │   └── loading.tsx                    # Loading skeleton
│   │
│   └── reports/                           # Raporlar (placeholder)
│       └── page.tsx
│
├── lib/
│   └── api.ts                             # API client (fetch wrappers)
│
├── public/                                # Static assets
│   ├── file.svg
│   ├── globe.svg
│   ├── next.svg
│   ├── vercel.svg
│   └── window.svg
│
├── .env.local                             # Environment variables
├── .env.local.example
├── .gitignore
├── package.json                           # Dependencies
├── package-lock.json
├── tsconfig.json                          # TypeScript config
├── next.config.ts                         # Next.js config
├── postcss.config.mjs                     # PostCSS config
├── eslint.config.mjs                      # ESLint config
├── next-env.d.ts
└── README.md
```

---

## ⚙️ Backend Yapısı (aura-backend/)

```
aura-backend/
├── app/                                   # FastAPI application
│   ├── __init__.py
│   ├── main.py                            # FastAPI app entry point
│   │
│   ├── api/                               # API endpoints
│   │   ├── __init__.py
│   │   ├── customers.py                   # Customer endpoints
│   │   ├── dashboard.py                   # Dashboard summary
│   │   ├── prediction.py                  # Risk prediction
│   │   └── simulation.py                  # ROI simulation
│   │
│   ├── services/                          # Business logic / ML services
│   │   ├── __init__.py
│   │   ├── churn_predictor.py            # Mock churn predictor (ACTIVE)
│   │   ├── churn_predictor_real.py       # Real XGBoost predictor (PASSIVE)
│   │   ├── shap_explainer.py             # Mock SHAP explainer (ACTIVE)
│   │   ├── shap_explainer_real.py        # Real SHAP explainer (PASSIVE)
│   │   ├── offer_optimizer.py            # Campaign recommendation
│   │   └── roi_simulator.py              # ROI calculation
│   │
│   ├── repositories/                      # Data access layer
│   │   ├── __init__.py
│   │   └── customer_repository.py        # Customer CRUD operations
│   │
│   ├── schemas/                           # Pydantic models
│   │   ├── __init__.py
│   │   └── customer.py                   # Request/Response schemas
│   │
│   ├── db/                                # Database
│   │   ├── __init__.py
│   │   ├── base.py                       # Database session
│   │   └── models.py                     # SQLAlchemy models
│   │
│   ├── core/                              # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py                     # Configuration
│   │   └── cache.py                      # Caching layer
│   │
│   └── tests/                             # Test directory (empty)
│
├── alembic/                               # Database migrations
│   ├── versions/
│   │   └── 77b19efadb26_initial_schema_customers_predictions_.py
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── models/                                # ML model files (EMPTY - will be filled after training)
│   └── .gitkeep
│
├── data/                                  # Data files
│   └── .gitkeep
│
├── venv/                                  # Python virtual environment
│
├── test_*.py                              # Test files (root level)
│   ├── test_api.py
│   ├── test_cache.py
│   ├── test_churn_predictor.py
│   ├── test_customer_repository.py
│   ├── test_integration.py
│   ├── test_offer_optimizer.py
│   ├── test_roi_simulator.py
│   └── test_shap_explainer.py
│
├── ML Training Files:                     # ML model training
│   ├── AURA_Model_Training_Colab.ipynb   # 🎯 READY NOTEBOOK (use this!)
│   ├── train_model.py                    # Alternative local training script
│   ├── ML_TRAINING_GUIDE.md              # Detailed training guide
│   ├── CHATGPT_PROMPT.md                 # ChatGPT assistant prompt (DETAILED)
│   ├── CHATGPT_PROMPT_SHORT.md           # ChatGPT assistant prompt (SHORT)
│   └── PROJECT_STRUCTURE.md              # This file
│
├── Configuration Files:
│   ├── .env                              # Environment variables
│   ├── .env.example
│   ├── .gitignore
│   ├── requirements.txt                  # Python dependencies
│   ├── alembic.ini                       # Alembic config
│   └── start_server.sh                   # Server start script
│
├── Database:
│   └── aura_dev.db                       # SQLite database (250 customers)
│
└── seed_database.py                      # Database seeding script
```

---

## 📊 Spec Dosyaları (.kiro/)

```
.kiro/
└── specs/
    └── aura-dashboard/
        ├── requirements.md               # Feature requirements
        ├── design.md                     # Design document
        └── tasks.md                      # Implementation tasks
```

---

## 🎯 ÖNEMLİ DOSYALAR (Model Eğitimi İçin)

### Şu Anda Kullanılan (Mock):
```
aura-backend/app/services/
├── churn_predictor.py        ✅ ACTIVE - Mock model (rule-based)
└── shap_explainer.py         ✅ ACTIVE - Mock SHAP (fake values)
```

### Eğitim Sonrası Kullanılacak (Real):
```
aura-backend/app/services/
├── churn_predictor_real.py   ⏸️  PASSIVE - Real XGBoost model
└── shap_explainer_real.py    ⏸️  PASSIVE - Real SHAP library
```

### Model Dosyaları (Eğitim Sonrası Oluşacak):
```
aura-backend/models/
├── churn_model.pkl           # Trained XGBoost model (~2MB)
├── churn_model.json          # Model in JSON format (~1MB)
├── scaler.pkl                # Feature scaler (~10KB)
├── label_encoders.pkl        # Categorical encoders (~5KB)
├── model_metrics.pkl         # Performance metrics (~1KB)
└── feature_names.pkl         # Feature names (~1KB)
```

---

## 🚀 ÇALIŞAN SERVİSLER

### Backend (Port 8000):
```bash
cd aura-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend (Port 3000):
```bash
cd aura-frontend
npm run dev
```

### Database:
```
SQLite: aura-backend/aura_dev.db
- 250 customers
- Prediction records
- Campaign catalog
```

---

## 📦 DEPENDENCIES

### Frontend (package.json):
```json
{
  "dependencies": {
    "next": "15.x",
    "react": "19.x",
    "recharts": "^2.x",
    "framer-motion": "^11.x"
  }
}
```

### Backend (requirements.txt):
```
fastapi
uvicorn
sqlalchemy
pydantic
python-dotenv
xgboost
scikit-learn
pandas
numpy
joblib
```

### ML Training (additional):
```
shap
matplotlib
seaborn
opendatasets
```

---

## 🎨 TEMA VE RENKLER

### Landing Page (Dark Theme):
- Background: `#0a0a1f`
- Gradient: Dark blue to purple

### Dashboard Pages (Light Theme - Jira Colors):
- Background: `#F4F5F7`
- Blue: `#0052CC`
- Green: `#00875A`
- Orange: `#FF991F`
- Red: `#DE350B`
- Purple: `#6554C0`

---

## 📊 VERİ AKIŞI

```
Frontend (Next.js)
    ↓ HTTP Request
Backend API (FastAPI)
    ↓ Business Logic
ML Services (Mock/Real)
    ↓ Predictions
Database (SQLite)
    ↓ Customer Data
Response → Frontend
```

---

## 🔄 MODEL EĞİTİM SONRASI DEĞİŞİKLİKLER

### Adım 1: Model Dosyalarını Koy
```bash
cd aura-backend
unzip models.zip
# models/ klasörü dolacak
```

### Adım 2: Mock Servisleri Yedekle
```bash
mv app/services/churn_predictor.py app/services/churn_predictor_mock.py
mv app/services/shap_explainer.py app/services/shap_explainer_mock.py
```

### Adım 3: Real Servisleri Aktif Et
```bash
mv app/services/churn_predictor_real.py app/services/churn_predictor.py
mv app/services/shap_explainer_real.py app/services/shap_explainer.py
```

### Adım 4: Backend'i Yeniden Başlat
```bash
# Ctrl+C ile durdur
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

---

## ✅ KONTROL LİSTESİ

### Şu Anda Çalışan:
- ✅ Frontend (Next.js 15) - Port 3000
- ✅ Backend (FastAPI) - Port 8000
- ✅ Database (SQLite) - 250 customers
- ✅ Mock ML models
- ✅ Dashboard, customer list, detail pages
- ✅ Risk calculator
- ✅ ROI simulator
- ✅ Recharts visualizations
- ✅ Responsive design
- ✅ Loading skeletons
- ✅ Turkish localization

### Model Eğitimi Sonrası Olacak:
- ⏳ Real XGBoost model
- ⏳ Real SHAP explanations
- ⏳ Trained model files (~5MB)
- ⏳ Better accuracy (~81%)
- ⏳ Production-ready ML

---

## 📝 NOTLAR

1. **Mock vs Real**: Şu anda mock model kullanılıyor, yarışma için yeterli ama gerçek model daha profesyonel
2. **Database**: SQLite kullanılıyor, production'da PostgreSQL önerilir
3. **Caching**: In-memory cache var, Redis eklenebilir
4. **Auth**: Şu anda yok, opsiyonel olarak eklenebilir
5. **Tests**: Test dosyaları var ama çoğu boş, geliştirilebilir

---

Bu yapıyı ChatGPT'ye gönder, projenin tam yapısını anlayacak!
