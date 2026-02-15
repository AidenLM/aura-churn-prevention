from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import dashboard, customers, prediction, simulation

app = FastAPI(
    title="AURA API",
    description="AI-powered Customer Churn Prevention System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router)
app.include_router(customers.router)
app.include_router(prediction.router)
app.include_router(simulation.router)

@app.get("/")
async def root():
    return {
        "message": "AURA API - Müşteri Kaybı Önleme Sistemi",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
