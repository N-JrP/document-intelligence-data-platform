from sentence_transformers import SentenceTransformer
import duckdb
import faiss
import numpy as np
import pickle
import os

DB_FILE = "warehouse/analytics.duckdb"
INDEX_FILE = "warehouse/faiss_index.bin"
DOCS_FILE = "warehouse/retrieval_docs.pkl"


def main():
    conn = duckdb.connect(DB_FILE)
    rows = conn.execute(
        """
        SELECT
            document_id,
            document_name,
            document_type,
            status,
            region,
            amount,
            summary,
            text
        FROM documents
        ORDER BY document_id
        """
    ).fetchall()
    conn.close()

    docs = []
    embedding_texts = []

    for row in rows:
        doc = {
            "document_id": row[0],
            "document_name": row[1],
            "document_type": row[2],
            "status": row[3],
            "region": row[4],
            "amount": row[5],
            "summary": row[6],
            "text": row[7],
        }
        docs.append(doc)
        embedding_texts.append(
            f"{doc['document_name']} {doc['document_type']} {doc['status']} {doc['region']} {doc['summary']} {doc['text']}"
        )

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(embedding_texts)

    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs("warehouse", exist_ok=True)
    faiss.write_index(index, INDEX_FILE)

    with open(DOCS_FILE, "wb") as f:
        pickle.dump(docs, f)

    print("FAISS index built successfully")


if __name__ == "__main__":
    main()