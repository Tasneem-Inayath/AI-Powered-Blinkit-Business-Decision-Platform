import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import joblib
from pathlib import Path

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Delivery Delay Risk (ML)", layout="wide")
st.header("🚚 Delivery Delay Prediction – Operations View")

MODEL_PATH = Path("data/delivery_delay_model.pkl")

# ---------------------------
# DB CONNECTION
# ---------------------------
@st.cache_data
def load_delay_data():  
    conn = psycopg2.connect(
        host="localhost",
        database="blinkit_db",
        user="postgres",
        password="2741"
    )

    query = """
    SELECT
        order_id,
        order_date,
        area,
        hour_of_day,
        day_of_week,
        is_weekend,
        order_total,
        total_items,
        promised_duration_minutes,
        is_late
    FROM ml_delivery_features;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


df = load_delay_data()
df["order_date"] = pd.to_datetime(df["order_date"])

# ---------------------------
# KPIs (OPS LEVEL)
# ---------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Avg Delay (mins)",
              f"{(df[df['is_late']==1]['promised_duration_minutes']).mean():.1f}")

with c2:
    st.metric("Late Order Rate",
              f"{df['is_late'].mean()*100:.1f}%")

with c3:
    st.metric("Orders Analysed",
              f"{len(df):,}")

st.info(
    "Model: Random Forest Classifier | "
    "Features: Area, Hour, Day, Order Size | "
    "Target: is_late (1 = delayed)"
)

# ---------------------------
# EDA – PATTERNS
# ---------------------------
st.subheader("📊 Delay Patterns")

col1, col2 = st.columns(2)

with col1:
    hour_late = df.groupby("hour_of_day")["is_late"].mean().reset_index()
    fig1 = px.bar(
        hour_late,
        x="hour_of_day",
        y="is_late",
        title="Late Rate by Hour of Day",
        labels={"is_late": "Late Rate"}
    )
    fig1.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    area_late = (
        df.groupby("area")["is_late"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
        .head(15)
    )

    fig2 = px.bar(
        area_late,
        x="area",
        y="is_late",
        title="Late Rate by Area (Top 15)",
        labels={"is_late": "Late Rate"}
    )
    fig2.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# RISK CALCULATOR (OPS TOOL)
# ---------------------------
st.divider()
st.subheader("⚠️ Delivery Risk Calculator (Before Order Assignment)")

if not MODEL_PATH.exists():
    st.error("ML model not found. Train the model first.")
    st.stop()

model = joblib.load(MODEL_PATH)

areas = sorted(df["area"].dropna().unique().tolist())

c1, c2, c3, c4 = st.columns(4)

with c1:
    area = st.selectbox("Area", areas)

with c2:
    hour = st.slider("Hour of Day", 0, 23, 18)

with c3:
    day = st.selectbox(
        "Day of Week",
        ["Sun(0)", "Mon(1)", "Tue(2)", "Wed(3)", "Thu(4)", "Fri(5)", "Sat(6)"],
        index=5
    )
    day_of_week = int(day.split("(")[1].split(")")[0])

with c4:
    promised = st.slider("Promised Time (mins)", 8, 30, 15)

# Input for model
X = pd.DataFrame([{
    "area": area,
    "hour_of_day": hour,
    "day_of_week": day_of_week,
    "is_weekend": 1 if day_of_week in [0,6] else 0,
    "order_total": df["order_total"].median(),
    "total_items": int(df["total_items"].median()),
    "promised_duration_minutes": promised
}])

risk = float(model.predict_proba(X)[:, 1][0])

st.metric("Predicted Delay Risk", f"{risk*100:.1f}%")

if risk >= 0.75:
    st.error("🚨 HIGH RISK – allocate extra riders / throttle promotions")
elif risk >= 0.45:
    st.warning("⚠️ MEDIUM RISK – monitor closely")
else:
    st.success("✅ LOW RISK – normal operations")

st.caption(
    "Note: This tool is designed for operations planning, "
    "not customer-facing use."
)
