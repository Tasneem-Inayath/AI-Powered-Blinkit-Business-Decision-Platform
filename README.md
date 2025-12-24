
## AI-Powered Blinkit Business Decision Platform

### Domain

Quick Commerce (Q-Commerce) · Marketing Analytics · Operations Intelligence · Business Intelligence

---

## Project Overview

Blinkit operates in a fast-paced quick commerce environment where data is generated across multiple departments:

* Marketing campaigns and ad spend
* Sales orders and revenue
* Delivery operations and delays
* Customer feedback and complaints

These datasets exist in silos, making decision-making reactive and slow.

### Goal

Build a **Unified Business Decision Platform** that:

* Calculates **Marketing ROI (ROAS)** accurately
* **Predicts delivery delays before they happen**
* Explains **why customers are unhappy** using Generative AI

---

## Architecture Overview (4-Layer Design)

### Layer 1 — Data Engineering (SQL Foundation)

**Problem**
Marketing data is aggregated daily, while orders are transactional. This granularity mismatch prevents direct ROI analysis.

**Solution**

* Aggregate orders to daily revenue
* Aggregate marketing spend to daily totals
* Join both on date
* Compute ROAS and operational KPIs

**Key Output**

* `master_analytical_view` (PostgreSQL View)

**Skills Used**

* SQL CTEs
* Aggregations
* Date-based joins
* Handling missing and zero-spend days

---

### Layer 2 — Analytics Dashboard (Rear-View Mirror)

**Problem**
Business managers cannot interpret thousands of SQL rows.

**Solution**
Interactive **Streamlit Dashboard** featuring:

* Dual-axis charts

  * Revenue (line)
  * Marketing Spend (bars)
* Date filters (Last 7 / 30 / 365 days)
* KPI cards:

  * Total Revenue
  * Total Spend
  * Average ROAS
  * Average Delivery Delay

**Business Insight Example**
If marketing spend increases while revenue remains flat, the campaign is underperforming.

---

### Layer 3 — Predictive Machine Learning (Windshield)

**Problem**
Dashboards show delivery delays only after customers complain.

**Solution**
A **Random Forest classification model** that predicts **delivery delay risk before dispatch**.

#### Target Variable

```
is_late = 1 → actual_delivery_time > promised_delivery_time  
is_late = 0 → delivered on time
```

#### Features Used (No Data Leakage)

* hour_of_day
* day_of_week
* area
* promised_duration_minutes

#### Model Choice

* **RandomForestClassifier**
* Handles non-linear patterns
* Robust on small and noisy datasets
* No feature scaling required

#### Evaluation Metric

* ROC-AUC (focus on risk ranking)

**Output**

* `delivery_delay_model.pkl`

---

### Layer 4 — Generative AI & RAG (The Brain)

**Problem**
SQL explains *what* happened but not *why*.
Customer feedback contains the real reasons, but it is unstructured text.

**Solution**
A **Retrieval Augmented Generation (RAG)** system that allows managers to ask natural language questions.

#### RAG Pipeline

1. Convert feedback text into vector embeddings
2. Retrieve relevant feedback using cosine similarity
3. Send retrieved text to an LLM for summarization

#### Example Question

```
Why are customers unhappy in the South Zone?
```

#### Example Output

* Root cause analysis
* Business impact (churn, revenue risk)
* Actionable operational recommendations

**LLM Used**

* Groq (LLaMA-3 Instant)

---

## Application Pages

| Page                     | Description               |
| ------------------------ | ------------------------- |
| Project Overview         | High-level explanation    |
| Data Engineering         | SQL aggregation logic     |
| Marketing ROI Dashboard  | Revenue vs Spend          |
| Delivery Risk Calculator | ML-based delay prediction |
| AI Business Assistant    | RAG-powered insights      |

---

## Tech Stack

* Backend: PostgreSQL
* Data Engineering: SQL (CTEs)
* Frontend: Streamlit
* Visualization: Plotly
* Machine Learning: scikit-learn (Random Forest)
* Generative AI: Groq API
* Embeddings: Sentence Transformers

---

## Project Structure

```
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
```

---

## API Setup (Groq)

### Get API Key

[https://console.groq.com/](https://console.groq.com/)

### Set Environment Variable

**Windows**

```powershell
setx GROQ_API_KEY "your_api_key_here"
```

**Mac / Linux**

```bash
export GROQ_API_KEY="your_api_key_here"
```

Restart terminal after setting.

---

## Run the Application

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

---

## Interview Summary

> Built an end-to-end business decision platform using SQL, Streamlit, Machine Learning, and Generative AI. Solved a real-world granularity mismatch for ROAS, predicted delivery delays using a Random Forest model, and implemented a RAG-based AI assistant to explain customer complaints in business terms.

---

## Project Status

Completed · Portfolio-Ready ·

---


