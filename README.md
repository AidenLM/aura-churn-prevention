# AURA - Müşteri Kaybı Önleme Sistemi

AI-powered customer churn prevention system for telecom companies with modern, interactive dashboard.

## Project Structure

```
.
├── aura-frontend/          # Next.js 14 frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── lib/              # Utilities and helpers
│
├── aura-backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── db/           # Database models
│   │   ├── models/       # Pydantic models
│   │   ├── schemas/      # Request/response schemas
│   │   └── services/     # Business logic
│   ├── models/           # ML models (XGBoost, preprocessor)
│   └── data/             # Sample data
│
└── .kiro/specs/          # Feature specifications
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Animations**: Framer Motion
- **Charts**: Recharts
- **State**: Zustand
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI
- **ML**: XGBoost + SHAP
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Auth**: JWT (python-jose)

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+

### Frontend Setup

```bash
cd aura-frontend
npm install
npm run dev
```

Frontend will run on http://localhost:3000

### Backend Setup

```bash
cd aura-backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will run on http://localhost:8000

### Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE aura_db;
```

2. Update `.env` file with your database credentials

3. Run migrations (coming in Task 2)

## Development

- Frontend: `npm run dev` in `aura-frontend/`
- Backend: `uvicorn app.main:app --reload` in `aura-backend/`
- Linting: `npm run lint` (frontend)

## Features

- 📊 **Ana Sayfa**: Dashboard with hero section and metrics
- 👤 **Müşteri Detayı**: Customer risk analysis with SHAP explanations
- 🧪 **Risk Hesapla**: Manual risk calculator
- 📈 **Kampanya Simülasyonu**: ROI forecasting

## License

Private - All rights reserved
