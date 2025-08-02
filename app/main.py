from fastapi import FastAPI
from app.cost_utils import (
    get_total_cost, get_cost_by_service,
    get_cost_by_date, get_top_services,
    check_high_cost_alert
)

# Explicitly set docs and redoc URLs so they're not disabled in deployment
app = FastAPI(
    title="Cloud Cost Tracker API",
    description="API for tracking and visualizing cloud costs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def root():
    return {"message": "Cloud Cost Tracker API is running"}

@app.get("/total-cost")
def total_cost():
    return {"total_cost": get_total_cost()}  

@app.get("/cost-by-service")
def cost_by_service():
    return get_cost_by_service()

@app.get("/cost-by-date")
def cost_by_date():
    return get_cost_by_date()

@app.get("/top-services")
def top_services(n: int = 5):
    return get_top_services(n)

@app.get("/high-cost-alert")
def high_cost_alert(threshold: float):
    return check_high_cost_alert(threshold)
