import duckdb
import pandas as pd

SILVER_FILE = "data/silver/documents.csv"
DB_FILE = "warehouse/analytics.duckdb"

def main():
    # connect to DuckDB (creates file if not exists)
    conn = duckdb.connect(DB_FILE)

    # load CSV into dataframe
    df = pd.read_csv(SILVER_FILE)

    # create table
    conn.execute("DROP TABLE IF EXISTS documents")
    conn.execute("CREATE TABLE documents AS SELECT * FROM df")

    conn.close()
    print("Data loaded into DuckDB successfully")

if __name__ == "__main__":
    main()