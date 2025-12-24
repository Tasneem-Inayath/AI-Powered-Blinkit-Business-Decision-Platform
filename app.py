import streamlit as st

st.set_page_config(
    page_title="AI-Powered Blinkit Decision Platform",
    layout="wide"
)

st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Project Overview",
        "🧱 Data Engineering (Layer 1)",
        "📣 Marketing ROI Dashboard",
        "🚚 Delivery Risk Calculator",
        "🧠 AI Business Assistant"
    ]
)

# =========================
# ROUTING
# =========================
if page == "🏠 Project Overview":
    st.title("🛒 AI-Powered Blinkit Business Decision Platform")

    st.markdown("""
    ### Unified Business Intelligence Platform

    This application connects:
    - **Marketing Analytics (ROAS)**
    - **Operations Intelligence (Delivery Risk)**
    - **Customer Intelligence (AI Assistant)**

    Built using:
    - PostgreSQL (SQL + CTEs)
    - Streamlit (Dashboards)
    - Machine Learning
    - Generative AI (RAG)
    """)

    st.info("⬅ Use the sidebar to navigate through project layers")

elif page == "🧱 Data Engineering (Layer 1)":
    st.switch_page("pages/data_eng.py")

elif page == "📣 Marketing ROI Dashboard":
    st.switch_page("pages/marketing.py")

elif page == "🚚 Delivery Risk Calculator":
    st.switch_page("pages/risk_calculator.py")

elif page == "🧠 AI Business Assistant":
    st.switch_page("pages/rag.py")
