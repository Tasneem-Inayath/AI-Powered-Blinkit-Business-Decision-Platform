import pandas as pd
import psycopg2

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# -----------------------------
# LOAD DATA FROM POSTGRES
# -----------------------------
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
    hour_of_day,
    day_of_week,
    is_weekend,
    area,
    order_total,
    total_items,
    promised_duration_minutes,
    is_late
FROM ml_delivery_features
ORDER BY order_date;
"""

df = pd.read_sql(query, conn)
conn.close()

# -----------------------------
# BASIC CLEANING
# -----------------------------
df = df.dropna(
    subset=[
        "area",
        "hour_of_day",
        "day_of_week",
        "promised_duration_minutes",
        "is_late"
    ]
)

# -----------------------------
# FEATURES & TARGET
# -----------------------------
X = df[
    ["area", "hour_of_day", "day_of_week", "promised_duration_minutes"]
].copy()

y = df["is_late"].astype(int)

# -----------------------------
# TRAIN / TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.22,
    random_state=42,
    stratify=y
)

# -----------------------------
# PREPROCESSING
# -----------------------------
pre = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["area"]),
        ("num", "passthrough",
         ["hour_of_day", "day_of_week", "promised_duration_minutes"])
    ]
)

# -----------------------------
# RANDOM FOREST MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=20,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# -----------------------------
# PIPELINE
# -----------------------------
pipe = Pipeline([
    ("pre", pre),
    ("model", model)
])

# -----------------------------
# TRAIN
# -----------------------------
pipe.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------
proba = pipe.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)

print("✅ Delay Risk Model trained")
print("Model: RandomForestClassifier")
print("Features: area, hour_of_day, day_of_week, promised_duration_minutes")

print("\n--- Classification Report ---")
print(classification_report(y_test, pred, digits=3))

print("ROC-AUC:", round(roc_auc_score(y_test, proba), 4))
import joblib
joblib.dump(pipe, "delivery_delay_model.pkl")
