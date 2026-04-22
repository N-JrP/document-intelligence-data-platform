import pickle
import duckdb
import faiss
import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer

DB_FILE = "warehouse/analytics.duckdb"
INDEX_FILE = "warehouse/faiss_index.bin"
DOCS_FILE = "warehouse/retrieval_docs.pkl"

st.set_page_config(page_title="Document Intelligence Data Platform", layout="wide")

st.title("Document Intelligence Data Platform")
st.write("End-to-end document intelligence platform with structured analytics and AI-powered retrieval")

conn = duckdb.connect(DB_FILE)

documents_df = conn.execute("SELECT * FROM documents ORDER BY document_id").df()
type_counts_df = conn.execute("SELECT * FROM dim_document_type_counts ORDER BY document_count DESC").df()
status_counts_df = conn.execute("SELECT * FROM dim_status_counts ORDER BY document_count DESC").df()
amounts_df = conn.execute("SELECT * FROM fct_amounts_by_type ORDER BY total_amount DESC").df()

conn.close()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Documents", len(documents_df))
col2.metric("Document Types", documents_df["document_type"].nunique())
col3.metric("Statuses", documents_df["status"].nunique())
col4.metric("Regions", documents_df["region"].nunique())

st.divider()

st.subheader("Filters")

filter_col1, filter_col2 = st.columns(2)

all_types = ["All"] + sorted(documents_df["document_type"].dropna().unique().tolist())
all_statuses = ["All"] + sorted(documents_df["status"].dropna().unique().tolist())

selected_type = filter_col1.selectbox("Filter by document type", all_types)
selected_status = filter_col2.selectbox("Filter by status", all_statuses)

filtered_df = documents_df.copy()

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["document_type"] == selected_type]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]

st.subheader("Structured Documents")
st.dataframe(filtered_df, use_container_width=True)

st.divider()

st.subheader("Analytics")

analytics_col1, analytics_col2 = st.columns(2)

with analytics_col1:
    st.write("Documents by Type")
    st.dataframe(type_counts_df, use_container_width=True)
    st.bar_chart(type_counts_df.set_index("document_type")["document_count"])

with analytics_col2:
    st.write("Documents by Status")
    st.dataframe(status_counts_df, use_container_width=True)
    st.bar_chart(status_counts_df.set_index("status")["document_count"])

st.write("Amounts by Document Type")
st.dataframe(amounts_df, use_container_width=True)

if not amounts_df.empty:
    st.bar_chart(amounts_df.set_index("document_type")["total_amount"])

st.divider()

st.subheader("Example Questions")
st.write("- Which claim documents are approved?")
st.write("- Which support issues are open?")
st.write("- What documents mention reimbursement?")
st.write("- Which travel documents have high amounts?")

st.divider()

st.subheader("Ask the documents")

question = st.text_input("Type your question here")
top_k = st.slider("Number of results", min_value=1, max_value=5, value=3)

if question:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(INDEX_FILE)

    with open(DOCS_FILE, "rb") as f:
        docs = pickle.load(f)

    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    distances, indices = index.search(question_embedding, k=top_k)

    matched_docs = []
    for rank, idx in enumerate(indices[0]):
        doc = docs[idx]
        score = float(distances[0][rank])
        matched_docs.append(
            {
                "document_name": doc["document_name"],
                "document_type": doc["document_type"],
                "status": doc["status"],
                "region": doc["region"],
                "amount": doc["amount"],
                "summary": doc["summary"],
                "text": doc["text"],
                "score": round(score, 4),
            }
        )

    results_df = pd.DataFrame(matched_docs)

    question_lower = question.lower()

    if "policy" in question_lower:
        filtered_results = results_df[results_df["document_type"] == "policy"]
        if not filtered_results.empty:
            results_df = filtered_results

    elif "claim" in question_lower or "insurance" in question_lower:
        filtered_results = results_df[results_df["document_type"] == "claim"]
        if not filtered_results.empty:
            results_df = filtered_results

    elif "support" in question_lower or "login" in question_lower or "password" in question_lower:
        filtered_results = results_df[results_df["document_type"] == "support"]
        if not filtered_results.empty:
            results_df = filtered_results

    elif "payment" in question_lower:
        filtered_results = results_df[results_df["document_type"] == "ticket"]
        if not filtered_results.empty:
            results_df = filtered_results

    elif "travel" in question_lower or "reimbursement" in question_lower:
        filtered_results = results_df[results_df["document_type"] == "travel"]
        if not filtered_results.empty:
            results_df = filtered_results

    st.subheader("AI Summary")
    if not results_df.empty:
        summary_text = (
            f"Retrieved {len(results_df)} relevant document(s). "
            f"Top matches mainly belong to document type(s): "
            f"{', '.join(results_df['document_type'].astype(str).unique())}. "
            f"Statuses found: {', '.join(results_df['status'].astype(str).unique())}."
        )
        st.write(summary_text)
    else:
        st.write("No relevant documents found.")

    st.subheader("Relevant Documents")
    for _, row in results_df.iterrows():
        with st.expander(f"{row['document_name']} | {row['document_type']} | score={row['score']}"):
            st.write(f"**Status:** {row['status']}")
            st.write(f"**Region:** {row['region']}")
            st.write(f"**Amount:** {row['amount']}")
            st.write(f"**Summary:** {row['summary']}")
            st.write(f"**Text:** {row['text']}")

    st.subheader("Retrieved Results Table")
    st.dataframe(results_df, use_container_width=True)