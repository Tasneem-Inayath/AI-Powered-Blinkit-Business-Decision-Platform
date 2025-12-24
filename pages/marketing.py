import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

# =======================
# PAGE CONFIG
# =======================
st.set_page_config(page_title="Marketing ROI (ROAS)", layout="wide")
st.header("📣 Marketing ROI (ROAS)")

# =======================
# DB CONNECTION
# =======================
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="blinkit_db",
        user="postgres",
        password="2741"
    )

# =======================
# LOAD DATA
# =======================
@st.cache_data
def load_roas_data():
    conn = get_connection()
    query = """
        SELECT
            date,
            total_revenue,
            total_spend,
            roas,
            avg_delay_minutes
        FROM master_analytical_view
        ORDER BY date;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_roas_data()
df["date"] = pd.to_datetime(df["date"])

if df.empty:
    st.warning("No data available")
    st.stop()

# =======================
# DATE FILTER (LIKE HERS)
# =======================
st.sidebar.header("📅 Date Filter")

today = df["date"].max().date()

filter_type = st.sidebar.selectbox(
    "Select Period",
    ["Last 7 Days", "Last 30 Days", "Last 1 Year", "Custom"]
)

if filter_type == "Last 7 Days":
    start = today - pd.Timedelta(days=7)
    end = today
elif filter_type == "Last 30 Days":
    start = today - pd.Timedelta(days=30)
    end = today
elif filter_type == "Last 1 Year":
    start = today - pd.Timedelta(days=365)
    end = today
else:
    start, end = st.sidebar.date_input( #type: ignore
        "Custom Range",
        [df["date"].min().date(), df["date"].max().date()]
    )

df = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)] #type:ignore 

# =======================
# KPI CARDS
# =======================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Revenue (₹)", f"{df['total_revenue'].sum()/1e5:.2f} L")

with c2:
    st.metric("Spend (₹)", f"{df['total_spend'].sum()/1e5:.2f} L")

with c3:
    spend = df["total_spend"].sum()
    roas = (df["total_revenue"].sum() / spend) if spend > 0 else None
    st.metric("ROAS", "—" if roas is None else f"{roas:.2f}x")

with c4:
    st.metric("Avg Delay", f"{df['avg_delay_minutes'].mean():.1f} mins")

# =======================
# EXPLANATION BOX (IMPORTANT)
# =======================
st.info(
    "This dashboard aligns **daily marketing spend** with **aggregated daily revenue**. "
    "Because orders do not contain a campaign ID, revenue is first summed per day and "
    "then joined with daily marketing spend to calculate ROAS. "
    "Managers can instantly spot days where spend increased but revenue stayed flat."
)

# =======================
# SPEND (BAR) + REVENUE (LINE)
# =======================
fig = px.bar(
    df,
    x="date",
    y="total_spend",
    title="Daily Marketing Spend (Bars) + Revenue (Line)",
    labels={"total_spend": "Ad Spend"}
)

line = px.line(df, x="date", y="total_revenue")
for trace in line.data:
    fig.add_trace(trace)

fig.update_layout(height=430)
st.plotly_chart(fig, use_container_width=True)

# =======================
# ROAS TREND
# =======================
fig2 = px.line(
    df,
    x="date",
    y="roas",
    markers=True,
    title="ROAS Trend (Daily)"
)
fig2.update_layout(height=340)
st.plotly_chart(fig2, use_container_width=True)

# =======================
# BEST ROAS DAYS
# =======================
st.subheader("🏆 Best ROAS Period")

best_roas = df["roas"].max()
best_days = df[df["roas"] == best_roas]

st.write(f"Highest ROAS achieved: **{best_roas:.2f}x**")

st.dataframe(
    best_days[["date", "total_revenue", "total_spend", "roas"]],
    use_container_width=True
)
