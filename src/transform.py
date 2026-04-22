import json
import os
import re
import pandas as pd

BRONZE_FILE = "data/bronze/documents.json"
SILVER_FILE = "data/silver/documents.csv"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_amount(text, fallback_amount):
    match = re.search(r"(\d+)\s*EUR", str(text), flags=re.IGNORECASE)
    if match:
        return float(match.group(1))

    try:
        return float(fallback_amount)
    except (TypeError, ValueError):
        return 0.0


def extract_issue_type(document_type, text):
    text_lower = str(text).lower()

    if document_type == "claim":
        return "insurance_claim"
    if document_type == "support":
        return "authentication_issue" if "password" in text_lower or "login" in text_lower else "support_issue"
    if document_type == "policy":
        return "policy_update"
    if document_type == "ticket":
        return "payment_incident" if "payment" in text_lower else "support_ticket"
    if document_type == "travel":
        return "travel_reimbursement"
    if document_type == "technical":
        return "data_quality_issue"

    return "other"


def generate_summary(text):
    words = str(text).split()
    return " ".join(words[:12]) + ("..." if len(words) > 12 else "")


def extract_company(text):
    match = re.search(r"(?:at|joined)\s+([A-Z][a-zA-Z0-9_-]+)", str(text))
    return match.group(1) if match else None


def transform(records):
    df = pd.DataFrame(records)

    df["amount"] = df.apply(lambda row: extract_amount(row["text"], row["amount_raw"]), axis=1)
    df["issue_type"] = df.apply(lambda row: extract_issue_type(row["document_type"], row["text"]), axis=1)
    df["summary"] = df["text"].apply(generate_summary)
    df["text_length"] = df["text"].astype(str).apply(len)
    df["name"] = df["text"].astype(str).str.split().str[1]
    df["company"] = df["text"].apply(extract_company)

    return df[
        [
            "document_id",
            "document_name",
            "document_type",
            "source_system",
            "status",
            "region",
            "amount",
            "issue_type",
            "summary",
            "text_length",
            "text",
            "name",
            "company",
        ]
    ]


def save_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def main():
    records = load_json(BRONZE_FILE)
    df = transform(records)
    save_csv(df, SILVER_FILE)
    print(f"Saved transformed data to {SILVER_FILE}")


if __name__ == "__main__":
    main()