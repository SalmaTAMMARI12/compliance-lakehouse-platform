from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="pipeline_conformite_dnssi",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dgssi"],
) as dag:

    extraction = BashOperator(
        task_id="extraction_audit",
        bash_command=(
            'cd /opt/airflow/project && '
            'PYTHONPATH=/opt/airflow/project/src '
            'python scripts/extraire_audit_depuis_silver.py "Exemple de rapport d\'audit.pdf"'
        ),
    )

    warehouse = BashOperator(
        task_id="etl_vers_warehouse",
        bash_command=(
            'cd /opt/airflow/project && '
            'PYTHONPATH=/opt/airflow/project/src '
            'python scripts/etl_vers_warehouse.py'
        ),
    )

    extraction >> warehouse
