# src/rag_chat.py
import streamlit as st
import pickle
import pandas as pd
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

# ==========================
# LOAD EMBEDDINGS & METADATA
# ==========================
with open("data/feedback_vectors.pkl", "rb") as f:
    embeddings = pickle.load(f)

metadata = pd.read_pickle("data/feedback_metadata.pkl")

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ==========================
# RETRIEVAL FUNCTION
# ==========================
def retrieve_feedbacks(query, top_k=5, min_score=0.35):
    query_vec = embed_model.encode([query])
    scores = cosine_similarity(query_vec, embeddings)[0]

    # Apply similarity threshold
    valid_idx = [
        i for i, score in enumerate(scores)
        if score >= min_score
    ]

    if not valid_idx:
        return pd.DataFrame()  # IMPORTANT: no hallucination

    # Sort by similarity
    top_idx = sorted(valid_idx, key=lambda i: scores[i], reverse=True)[:top_k]

    return metadata.iloc[top_idx]

# ==========================
# GROQ CLIENT
# ==========================
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ==========================
# ANSWER GENERATION
# ==========================
def generate_answer(question, retrieved_texts):
    context = "\n".join(f"- {t}" for t in retrieved_texts)

    prompt = f"""
You are an internal Business Intelligence Analyst at Blinkit.

You support Operations and Management teams.
You do NOT answer like customer support.
You do NOT guess beyond the data provided.

Below are real customer feedback comments from Blinkit users.
Analyze them strictly as operational signals.

Customer Feedback:
{context}

Manager Question:
{question}

Instructions:
- Identify the primary operational root causes
- Explain the impact on business metrics (delay, churn, satisfaction, revenue)
- Keep the explanation concise and decision-oriented
- If the data is insufficient, clearly say so

Respond in clear business terms suitable for leadership review.

"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

# ==========================
# STREAMLIT UI
# ==========================
st.set_page_config(page_title="Blinkit AI Assistant", layout="centered")
st.title("🧠 Blinkit AI Business Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

question = st.chat_input("Ask a business question…")

if question:
    st.session_state.chat.append(("user", question))

    retrieved = retrieve_feedbacks(question)

    if retrieved.empty:
        answer = "I don’t have enough customer feedback data to answer this question."
    else:
        answer = generate_answer(
            question,
            retrieved["clean_text"].tolist()
        )

    st.session_state.chat.append(("assistant", answer))

# ==========================
# CHAT HISTORY
# ==========================
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.write(msg)
