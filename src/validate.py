import duckdb

DB_FILE = "warehouse/analytics.duckdb"


def run_check(conn, label, query):
    result = conn.execute(query).fetchone()[0]
    print(f"{label}: {result}")
    return result


def main():
    conn = duckdb.connect(DB_FILE)

    total_rows = run_check(conn, "Total rows in documents", "SELECT COUNT(*) FROM documents")
    null_ids = run_check(conn, "Null document_id count", "SELECT COUNT(*) FROM documents WHERE document_id IS NULL")
    null_names = run_check(conn, "Null document_name count", "SELECT COUNT(*) FROM documents WHERE document_name IS NULL")
    empty_text = run_check(conn, "Empty text count", "SELECT COUNT(*) FROM documents WHERE TRIM(text) = ''")
    duplicate_names = run_check(
        conn,
        "Duplicate document_name count",
        """
        SELECT COUNT(*) FROM (
            SELECT document_name
            FROM documents
            GROUP BY document_name
            HAVING COUNT(*) > 1
        )
        """,
    )
    invalid_amounts = run_check(conn, "Negative amount count", "SELECT COUNT(*) FROM documents WHERE amount < 0")
    null_types = run_check(conn, "Null document_type count", "SELECT COUNT(*) FROM documents WHERE document_type IS NULL")

    failed = any([
        total_rows == 0,
        null_ids > 0,
        null_names > 0,
        empty_text > 0,
        duplicate_names > 0,
        invalid_amounts > 0,
        null_types > 0,
    ])

    if failed:
        print("Validation failed")
    else:
        print("Validation passed successfully")

    conn.close()


if __name__ == "__main__":
    main()