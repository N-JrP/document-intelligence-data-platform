\# Document Intelligence Data Platform



End-to-end local data platform that ingests unstructured documents, transforms them into structured datasets, models them in DuckDB with dbt, validates data quality, and serves an AI-powered retrieval interface using embeddings and FAISS.



\## Features



\- Raw-to-bronze-to-silver data pipeline

\- Structured metadata extraction

\- DuckDB warehouse

\- dbt staging and mart models

\- Data quality checks

\- Embeddings + FAISS retrieval

\- Streamlit analytics and Q\&A app

\- One-command pipeline execution



\## Tech Stack



\- Python

\- SQL

\- DuckDB

\- dbt

\- Streamlit

\- Sentence Transformers

\- FAISS

\- Pandas



\## Project Structure



document-intelligence-data-platform/

├── data/

│   ├── raw/

│   ├── bronze/

│   └── silver/

├── src/

│   ├── ingest.py

│   ├── transform.py

│   ├── load\_warehouse.py

│   ├── validate.py

│   ├── build\_index.py

│   ├── run\_pipeline.py

│   └── app.py

├── warehouse/

├── dbt\_project/

│   └── models/

├── requirements.txt

├── .gitignore

└── README.md



\## Data Model



Each document is processed into these fields:



\- document\_id

\- document\_name

\- document\_type

\- source\_system

\- status

\- region

\- amount

\- issue\_type

\- summary

\- text\_length

\- text



\## Example Business Questions



\- Which claim documents are approved?

\- Which support issues are open?

\- What documents mention reimbursement?

\- Which travel documents have high amounts?



\## How to Run



\### 1. Activate environment

conda activate doc\_rag\_project



\### 2. Run full pipeline

python src\\run\_pipeline.py



\### 3. Start the app

streamlit run src\\app.py



\## What This Project Demonstrates



\- Python-based ETL/ELT

\- SQL modeling

\- Data warehousing with DuckDB

\- dbt transformations

\- Validation and data quality checks

\- RAG / embeddings / vector search

\- AI-assisted document retrieval

\- Basic product analytics dashboard

