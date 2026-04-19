# 🚀 AI-Powered Blinkit Business Decision Platform

### Domain  
Quick Commerce (Q-Commerce) · Marketing Analytics · Operations Intelligence · Business Intelligence  

---

## 📖 Project Overview
Blinkit operates in a fast-paced quick commerce environment where data is generated across multiple departments:

- Marketing campaigns and ad spend  
- Sales orders and revenue  
- Delivery operations and delays  
- Customer feedback and complaints  

These datasets exist in silos, making decision-making reactive and slow.  

### 🎯 Goal
Build a **Unified Business Decision Platform** that:  
- Calculates **Marketing ROI (ROAS)** accurately  
- **Predicts delivery delays before they happen**  
- Explains **why customers are unhappy** using Generative AI  

---

## 🏗️ Architecture Overview (4-Layer Design)

### Layer 1 — Data Engineering (SQL Foundation)
- Aggregate orders to daily revenue  
- Aggregate marketing spend to daily totals  
- Join both on date  
- Compute ROAS and operational KPIs  

**Output:** `master_analytical_view` (PostgreSQL View)  

---

### Layer 2 — Analytics Dashboard (Rear-View Mirror)
Interactive **Streamlit Dashboard** featuring:  
- Dual-axis charts (Revenue vs Marketing Spend)  
- Date filters (Last 7 / 30 / 365 days)  
- KPI cards (Revenue, Spend, ROAS, Delivery Delay)  

---

### Layer 3 — Predictive Machine Learning (Windshield)
- **Random Forest model** predicts delivery delay risk before dispatch  
- Features: hour_of_day, day_of_week, area, promised_duration_minutes  
- Metric: ROC-AUC  

**Output:** `delivery_delay_model.pkl`  

---

### Layer 4 — Generative AI & RAG (The Brain)
- Feedback embeddings with Sentence Transformers  
- Cosine similarity retrieval  
- Summarization via Groq LLaMA-3 Instant  

**Example Question:**  
> Why are customers unhappy in the South Zone?  

---

## 🌐 Live Demo
Deployed on **Render**:  
[AI-Powered Blinkit Business Decision Platform](https://ai-powered-blinkit-business-decision.onrender.com/)  

---

## 📊 Application Pages
| Page                     | Description               |
| ------------------------ | ------------------------- |
| Project Overview         | High-level explanation    |
| Data Engineering         | SQL aggregation logic     |
| Marketing ROI Dashboard  | Revenue vs Spend          |
| Delivery Risk Calculator | ML-based delay prediction |
| AI Business Assistant    | RAG-powered insights      |

---

## 🛠️ Tech Stack
- **Backend:** PostgreSQL  
- **Data Engineering:** SQL (CTEs)  
- **Frontend:** Streamlit  
- **Visualization:** Plotly  
- **Machine Learning:** scikit-learn (Random Forest)  
- **Generative AI:** Groq API  
- **Embeddings:** Sentence Transformers  

---

## 📂 Project Structure
sql/
└── master_analytical_view.sql

src/
├── app.py
├── marketing_dashboard.py
├── risk_calculator.py
├── rag_chat.py
├── train_delay_model.py

data/
├── feedback_vectors.pkl
├── feedback_metadata.pkl

---

## 🔑 API Setup (Groq)
1. Get API Key → [Groq Console](https://console.groq.com/)  
2. Set Environment Variable:  

**Windows**
```powershell
setx GROQ_API_KEY "your_api_key_here"

export GROQ_API_KEY="your_api_key_here"
```
**Run Locally**
pip install -r requirements.txt
streamlit run src/app.py
Here’s the section you wanted, formatted as a proper Markdown block so you can paste it directly into your `README.md` file:

``` ```
## ☁️ Deployment on Render

This project is deployed on **Render** for free hosting and continuous integration with GitHub.

### Steps
1. Added `requirements.txt` with dependencies  
2. Added `runtime.txt` to pin Python version (`python-3.10.12`)  
3. Added `Procfile` with Streamlit start command:
   ```
   web: streamlit run src/app.py --server.port=$PORT --server.headless=true
   ```
4. Connected GitHub repo to Render  
5. Configured build command:
   ```
   pip install -r requirements.txt
   ```
6. Automatic redeploy on every `git push`  

---

## 📌 Interview Summary

Built an end-to-end business decision platform using SQL, Streamlit, Machine Learning, and Generative AI. Solved a real-world granularity mismatch for ROAS, predicted delivery delays using a Random Forest model, and implemented a RAG-based AI assistant to explain customer complaints in business terms.  

---

## 📈 Project Status

✅ Completed · Portfolio-Ready  
```

