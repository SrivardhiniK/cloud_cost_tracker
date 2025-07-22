import pandas as pd

# Load the CSV billing data
from app.mock_cloud_api import generate_mock_billing_data
df = generate_mock_billing_data()

def get_total_cost():
    return round(df["Cost"].sum(), 2)

def get_cost_by_service():
    return df.groupby("Service")["Cost"].sum().round(2).to_dict()
def check_high_cost_alert(threshold: float):
    total_cost = get_total_cost()
    if total_cost > threshold:
        return {
            "alert": True,
            "message": f"⚠️ High cost alert! Total cost is ${total_cost} which exceeds the threshold of ${threshold}"
        }
    else:
        return {
            "alert": False,
            "message": f"✅ Cost is under control: ${total_cost}"
        }
    
def get_cost_by_date():
    grouped = df.groupby("Date")["Cost"].sum().reset_index()
    grouped = grouped.sort_values("Date")
    result = []
    for _, row in grouped.iterrows():
        result.append({
            "date": row["Date"],
            "cost": round(row["Cost"], 2)
        })
    return result
def get_top_services(n: int = 5):
    grouped = df.groupby("Service")["Cost"].sum().reset_index()
    grouped = grouped.sort_values("Cost", ascending=False).head(n)
    result = []
    for _, row in grouped.iterrows():
        result.append({
            "service": row["Service"],
            "cost": round(row["Cost"], 2)
        })
    return result

