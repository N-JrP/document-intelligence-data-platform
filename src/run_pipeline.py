import subprocess
import sys
from datetime import datetime


def run_command(step_name, command):
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] START: {step_name}")
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FAILED: {step_name}")
        sys.exit(result.returncode)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SUCCESS: {step_name}")


def main():
    print("=" * 60)
    print("DOCUMENT INTELLIGENCE PIPELINE ORCHESTRATION STARTED")
    print("=" * 60)

    run_command("Ingestion", "python src\\ingest.py")
    run_command("Transformation", "python src\\transform.py")
    run_command("Warehouse Load", "python src\\load_warehouse.py")
    run_command("dbt Modeling", "cd dbt_project && dbt run")
    run_command("Validation", "python src\\validate.py")
    run_command("Vector Index Build", "python src\\build_index.py")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()