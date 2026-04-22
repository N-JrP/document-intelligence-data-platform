import os
import json

RAW_FILE = "data/raw/documents.txt"
BRONZE_FILE = "data/bronze/documents.json"


def read_documents(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]


def make_records(lines):
    records = []

    for i, line in enumerate(lines, start=1):
        parts = line.split("|", 6)

        document_name = parts[0].strip() if len(parts) > 0 else f"doc_{i:03d}"
        document_type = parts[1].strip() if len(parts) > 1 else "unknown"
        source_system = parts[2].strip() if len(parts) > 2 else "unknown"
        status = parts[3].strip() if len(parts) > 3 else "unknown"
        region = parts[4].strip() if len(parts) > 4 else "unknown"
        amount = parts[5].strip() if len(parts) > 5 else "0"
        text = parts[6].strip() if len(parts) > 6 else ""

        records.append(
            {
                "document_id": i,
                "document_name": document_name,
                "document_type": document_type,
                "source_system": source_system,
                "status": status,
                "region": region,
                "amount_raw": amount,
                "text": text,
            }
        )

    return records


def save_json(records, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def main():
    lines = read_documents(RAW_FILE)
    records = make_records(lines)
    save_json(records, BRONZE_FILE)
    print(f"Saved {len(records)} records to {BRONZE_FILE}")


if __name__ == "__main__":
    main()