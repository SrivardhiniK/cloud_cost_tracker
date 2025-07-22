from fastapi import FastAPI
from app.cost_utils import (
    get_total_cost, get_cost_by_service,
    get_cost_by_date, get_top_services,
    check_high_cost_alert
)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Cloud Cost Tracker API is running"}

@app.get("/total-cost")
def total_cost():
    return {"total_cost": get_total_cost()}  # <-- FIXED: wrapped in a dict

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
