# Document Intelligence Data Platform

End-to-end data platform for transforming unstructured business documents into structured analytics and AI-powered search.

---

## 🚀 Live App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]((https://document-intelligence-data-platform-ed9qdjyfap3qg7cyow5f6w.streamlit.app/))

---

## 🧠 Business Problem

Organizations store critical operational data in unstructured formats such as:
- insurance claims
- support tickets
- policy documents
- incident reports

This makes it difficult to:
- analyze trends
- extract insights
- search information efficiently

---

## 💡 Solution

This project converts unstructured documents into a structured data platform and enables semantic AI search.

It combines:
- data engineering pipeline
- analytics modeling
- AI-based document retrieval

---

## ⚙️ What it does

- Ingests raw document data  
- Extracts structured fields (type, status, region, amount)  
- Loads into DuckDB warehouse  
- Builds analytics models using dbt  
- Runs data quality checks  
- Creates embeddings for semantic search  
- Provides Streamlit dashboard + AI query interface  

---

## 📊 Business Impact

- Faster document search using AI retrieval  
- Structured analytics from unstructured data  
- Improved visibility into claims, support, and incidents  
- Enables decision-making using real-time insights  

---

## 🛠 Tech Stack

Python • SQL • DuckDB • dbt • Pandas • Streamlit • FAISS • Sentence Transformers

---

## 📈 Key Features

- ETL pipeline (raw → bronze → silver → warehouse)  
- dbt models (staging + marts)  
- data quality validation  
- analytics dashboards (counts, amounts)  
- AI document retrieval (RAG-style search)  
- filtering by document type & status  
- similarity-based search results  

---

## 🔍 Example Queries

- insurance claim  
- payment failure  
- travel reimbursement  
- login issue  
- policy update Berlin  

---

## ▶️ Run Locally

```bash
conda activate doc_rag_project
python src\run_pipeline.py
streamlit run src\app.py
```
---

## 🔮 Future Improvements

- Add real-time data ingestion (API / streaming)
- Improve retrieval with hybrid search (metadata + embeddings)
- Deploy using scalable cloud data warehouse (BigQuery / Snowflake)
