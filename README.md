# AURA - Müşteri Kaybı Önleme Sistemi

AI destekli müşteri kaybı tahmin ve önleme platformu. TrustedModel Telco Customer Churn dataset'i kullanılarak geliştirilmiştir.

## 🌐 Live Demo

**Production URL:** https://nativestruct.com

- Frontend: Vercel (Next.js 15)
- Backend: Render (FastAPI Python)
- Database: SQLite (100 müşteri verisi)

## 🏗️ Proje Yapısı

```
aura-churn-prevention/
├── aura-frontend/          # Next.js 15 + React 19 + Tailwind CSS 4
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── lib/              # API client & utilities
├── aura-backend/          # FastAPI Python backend
│   ├── app/              # Application code
│   │   ├── api/         # API endpoints
│   │   ├── services/    # ML services
│   │   ├── db/          # Database models
│   │   └── core/        # Configuration
│   ├── models/          # ML model files
│   └── TrustedModel/    # Dataset
└── .kiro/               # Spec files
```

## 🚀 Local Development

### Backend Setup

```bash
cd aura-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Load data (first time only)
python load_csv_data.py

# Start server
uvicorn app.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### Frontend Setup

```bash
cd aura-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: http://localhost:3000

## 📊 Features

1. **Dashboard** - Müşteri risk istatistikleri ve dağılımı
2. **Müşteri Listesi** - Tüm müşterilerin risk skorları
3. **Müşteri Detayı** - SHAP analizi ve AI önerileri
4. **Risk Hesaplama** - Yeni müşteri risk tahmini
5. **ROI Simülasyonu** - Kampanya maliyet analizi

## 🔧 Configuration

### Backend (.env)

```env
DATABASE_URL=sqlite:///./aura_dev.db
FRONTEND_URL=http://localhost:3000
MODEL_PATH=./models/best_model.pkl
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production (Vercel Environment Variables)

```env
NEXT_PUBLIC_API_URL=https://aura-churn-prevention.onrender.com
```

## 🎯 ML Model

- **Dataset:** TrustedModel Telco Customer Churn (7043 customers, 19 features)
- **Algorithm:** Voting Classifier (Random Forest + Gradient Boosting + Logistic Regression)
- **Accuracy:** 82.4%
- **ROC-AUC:** 0.87
- **Features:** 19 (demographic, account, services)

## 📦 Deployment

### Frontend (Vercel)

```bash
# Already deployed - auto-deploys on git push
# URL: https://nativestruct.com
```

### Backend (Render)

```bash
# Already deployed - auto-deploys on git push
# URL: https://aura-churn-prevention.onrender.com
```

## 🔗 API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `GET /api/dashboard/summary` - Dashboard stats
- `GET /api/customers/all/list` - All customers
- `GET /api/customers/{id}` - Customer detail
- `POST /api/predict/calculate` - Risk calculation
- `POST /api/simulation/roi` - ROI simulation

## 📝 Notes

- **CORS:** Production domains (nativestruct.com) and localhost both supported
- **Database:** SQLite for both local and production (simple deployment)
- **Free Tier:** Render free instance spins down after inactivity (50s cold start)
- **Data:** 100 customers loaded from TrustedModel CSV

## 🛠️ Tech Stack

**Frontend:**
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS 4
- Recharts (charts)

**Backend:**
- FastAPI (Python)
- SQLAlchemy (ORM)
- Scikit-learn (ML)
- Pandas (data processing)

**Deployment:**
- Vercel (frontend)
- Render (backend)
- GitHub (version control)

## 📄 License

MIT License - Developed for competition submission.
