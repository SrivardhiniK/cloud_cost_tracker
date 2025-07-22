import pandas as pd
import random
from datetime import datetime, timedelta

services = ["Compute Engine", "Cloud Storage", "BigQuery", "Cloud Functions", "VPC", "Cloud SQL"]

def generate_mock_billing_data(days=30):
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        for service in services:
            cost = round(random.uniform(0.5, 5.0), 2)
            data.append({
                "Date": date,
                "Service": service,
                "Cost": cost
            })
    df = pd.DataFrame(data)
    return df
