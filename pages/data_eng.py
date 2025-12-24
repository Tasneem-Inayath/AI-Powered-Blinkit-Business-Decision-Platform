import streamlit as st
import psycopg2
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Data Engineering",
    layout="wide"
)

st.title("Data Engineering (Foundation)")
st.caption("Turning raw multi-source data into a single analytical truth")

# =========================
# DATABASE CONNECTION
# =========================
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="blinkit_db",
        user="postgres",
        password="2741"
    )

# =========================
# PROBLEM EXPLANATION
# =========================
st.markdown("""
### ❓ The Real-World Problem

Blinkit data comes from **different teams**:

- **Marketing** → Daily ad spend (1 row per day)
- **Orders** → Transactional data (1000s of rows per day)

These **cannot be joined directly** due to **granularity mismatch**.

---

### ✅ SQL Solution

1. Aggregate orders **by date**
2. Aggregate marketing spend **by date**
3. Join on `date`
4. Compute business metrics (Revenue, ROAS, Delays)

The output is a **Master Analytical View**.
""")

# =========================
# CHART 1: RAW ORDERS VOLUME
# =========================
st.subheader("📦 Raw Orders Volume (Before Aggregation)")

@st.cache_data
def load_orders_daily_count():
    conn = get_connection()
    query = """
        SELECT
            DATE(order_date) AS date,
            COUNT(*) AS orders_count
        FROM blinkit_orders_clean
        GROUP BY DATE(order_date)
        ORDER BY date;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

orders_daily = load_orders_daily_count()
st.bar_chart(orders_daily.set_index("date")["orders_count"])

st.caption("Each bar represents hundreds/thousands of order rows per day")

# =========================
# CHART 2: MARKETING DATA
# =========================
st.subheader("📣 Marketing Spend (Already Daily)")

@st.cache_data
def load_marketing_daily():
    conn = get_connection()
    query = """
        SELECT
            date,
            SUM(spend) AS total_spend
        FROM blinkit_marketing_performance
        GROUP BY date
        ORDER BY date;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

marketing_daily = load_marketing_daily()
st.line_chart(marketing_daily.set_index("date")["total_spend"])

st.caption("Marketing data is already aggregated at daily level")

# =========================
# CHART 3: MASTER VIEW
# =========================
st.subheader("🧩 Master Analytical View (After SQL Aggregation & Join)")

@st.cache_data
def load_master_view():
    conn = get_connection()
    query = """
        SELECT
            date,
            total_orders,
            total_revenue
        FROM master_analytical_view
        ORDER BY date;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

master_df = load_master_view()

col1, col2 = st.columns(2)

with col1:
    st.line_chart(master_df.set_index("date")["total_orders"])
    st.caption("One row per day → total orders")

with col2:
    st.line_chart(master_df.set_index("date")["total_revenue"])
    st.caption("One row per day → total revenue")

# =========================
# SHOW SAMPLE DATA
# =========================
st.subheader("📊 Sample Output: Master Analytical View")

st.dataframe(
    master_df.head(10),
    use_container_width=True
)

# =========================
# INTERVIEW FLEX
# =========================
st.success("""
🎤 Interview Explanation:

"I resolved a real-world granularity mismatch by aggregating transactional
order data to daily level and joining it with time-series marketing data
using SQL CTEs. This master view acts as the foundation for analytics,
machine learning, and GenAI layers."
""")
