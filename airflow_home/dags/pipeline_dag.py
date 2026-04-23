from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "neha",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="document_intelligence_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    ingest = BashOperator(
        task_id="ingest",
        bash_command="python src/ingest.py",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="python src/transform.py",
    )

    load = BashOperator(
        task_id="load",
        bash_command="python src/load_warehouse.py",
    )

    validate = BashOperator(
        task_id="validate",
        bash_command="python src/validate.py",
    )

    build_index = BashOperator(
        task_id="build_index",
        bash_command="python src/build_index.py",
    )

    ingest >> transform >> load >> validate >> build_index