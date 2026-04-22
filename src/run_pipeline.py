import subprocess
import sys


def run_command(command):
    print(f"\nRunning: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        sys.exit(result.returncode)


def main():
    run_command("python src\\ingest.py")
    run_command("python src\\transform.py")
    run_command("python src\\load_warehouse.py")
    run_command("cd dbt_project && dbt run")
    run_command("python src\\validate.py")
    run_command("python src\\build_index.py")
    print("\nPipeline completed successfully")


if __name__ == "__main__":
    main()