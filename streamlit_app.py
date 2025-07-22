import streamlit as st
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8000"

# --- Column Normalization Helper ---
def normalize_columns(df):
    column_map = {
        "Date": ["date", "DATE", "Date"],
        "Service": ["service", "services", "Service", "cloud_service"],
        "UsageHours": ["usage", "Usage", "usage_hrs", "UsageHours"],
        "Cost": ["cost", "Cost", "total_cost", "Amount"],
        "Region": ["region", "Region", "zone", "location"]
    }

    renamed = {}
    for standard, variants in column_map.items():
        for v in variants:
            if v in df.columns:
                renamed[v] = standard
                break

    df.rename(columns=renamed, inplace=True)
    return df

# --- Streamlit Setup ---
st.set_page_config(page_title="Cloud Cost Tracker", layout="wide")
st.title("☁️ Cloud Cost Tracker Dashboard")

# --- Sidebar Options ---
st.sidebar.header("⚙️ Options")

if "use_upload" not in st.session_state:
    st.session_state.use_upload = False

# Toggle: Use Uploaded CSV
use_upload = st.sidebar.checkbox("📂 Use uploaded CSV", value=st.session_state.use_upload)
st.session_state.use_upload = use_upload

df_uploaded = None
uploaded_file = None

if use_upload:
    uploaded_file = st.sidebar.file_uploader("Upload Cloud Billing CSV", type=["csv"])

    if uploaded_file:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            df_uploaded = normalize_columns(df_uploaded)
            st.sidebar.success("✅ File uploaded and normalized!")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to read file: {e}")
    else:
        df_uploaded = None

    if st.sidebar.button("🔄 Reset to API Mode"):
        st.session_state.use_upload = False
        st.rerun()

# --- Total Cost ---
st.header("💰 Total Cloud Spend")
if df_uploaded is not None:
    total_cost = round(df_uploaded["Cost"].sum(), 2)
    st.metric(label="Total Cost", value=f"${total_cost:.2f}")
else:
    total = requests.get(f"{BASE_URL}/total-cost").json()
    st.metric(label="Total Cost", value=f"${total['total_cost']:.2f}")

# --- Cost by Date ---
st.header("📈 Daily Cost Trend")
if df_uploaded is not None:
    df_by_date = df_uploaded.groupby("Date")["Cost"].sum().reset_index()
    df_by_date = df_by_date.sort_values("Date")
else:
    by_date = requests.get(f"{BASE_URL}/cost-by-date").json()
    df_by_date = pd.DataFrame(by_date)
st.line_chart(df_by_date.set_index("Date" if df_uploaded is not None else "date"))

# --- Cost by Service ---
st.header("📊 Cost by Service")
if df_uploaded is not None:
    df_service = df_uploaded.groupby("Service")["Cost"].sum().reset_index()
    df_service.columns = ["service", "cost"]
else:
    by_service = requests.get(f"{BASE_URL}/cost-by-service").json()
    df_service = pd.DataFrame(list(by_service.items()), columns=["service", "cost"])
st.bar_chart(df_service.set_index("service"))

# --- Top Services ---
st.header("🏆 Top Expensive Services")
n = st.slider("Select top N services", 1, 10, 5)
if df_uploaded is not None:
    top_services_df = (
        df_uploaded.groupby("Service")["Cost"].sum().reset_index()
        .sort_values("Cost", ascending=False)
        .head(n)
    )
    top_services_df.columns = ["service", "cost"]
else:
    top_services = requests.get(f"{BASE_URL}/top-services", params={"n": n}).json()
    top_services_df = pd.DataFrame(top_services)
st.table(top_services_df)

# --- High Cost Alert ---
st.header("🚨 High Cost Alert")
threshold = st.number_input("Set alert threshold ($)", value=100.0)
if df_uploaded is not None:
    total_cost = round(df_uploaded["Cost"].sum(), 2)
    if total_cost > threshold:
        st.error(f"⚠️ High cost alert! Total cost is ${total_cost} which exceeds the threshold of ${threshold}")
    else:
        st.success(f"✅ Cost is under control: ${total_cost}")
else:
    alert = requests.get(f"{BASE_URL}/high-cost-alert", params={"threshold": threshold}).json()
    if alert["alert"]:
        st.error(alert["message"])
    else:
        st.success(alert["message"])
