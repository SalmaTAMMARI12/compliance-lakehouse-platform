# pyrefly: ignore [missing-import]
from airflow import DAG
# pyrefly: ignore [missing-import]
from airflow.operators.bash import BashOperator
from datetime import datetime

# ── Chemins dans le conteneur ─────────────────────────────
PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = f"{PROJECT_DIR}/dbt_project"

# ── Variables d'environnement injectées dans chaque BashOperator ──
# Permettent aux scripts Python et à dbt de joindre les services Docker
ENV_VARS = (
    "POSTGRES_HOST=dgssi-postgres "
    "POSTGRES_PORT=5432 "
    "POSTGRES_DB=$POSTGRES_DB "
    "POSTGRES_USER=$POSTGRES_USER "
    "POSTGRES_PASSWORD=$POSTGRES_PASSWORD "
    "MINIO_ENDPOINT=dgssi-minio:9000 "
    "MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY "
    "MINIO_SECRET_KEY=$MINIO_SECRET_KEY "
)

with DAG(
    dag_id="pipeline_conformite_dnssi",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dgssi", "conformite", "dnssi"],
    doc_md="""
    ## Pipeline de conformité DGSSI

    Charge les données dans PostgreSQL (ETL), puis exécute
    la transformation dbt et valide les tests qualité.

    **Flux** : `etl_vers_warehouse → dbt_run → dbt_test`

    > **Note** : L'extraction Docling (Bronze → Silver → Gold → Postgres)
    > est exécutée manuellement depuis le venv local car elle nécessite
    > SQLAlchemy 2.x + Docling, incompatibles avec Airflow.
    """,
) as dag:

    # ── Étape 1 : ETL vers le warehouse ─────────────────
    # Utilise psycopg2 directement (pas de SQLAlchemy 2.x)
    etl_warehouse = BashOperator(
        task_id="etl_vers_warehouse",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"{ENV_VARS} "
            f"PYTHONPATH={PROJECT_DIR}/src "
            "python scripts/etl_vers_warehouse.py"
        ),
    )

    # ── Étape 2 : dbt run ───────────────────────────────
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"cd {DBT_DIR} && "
            f"{ENV_VARS} "
            f"dbt run --profiles-dir {DBT_DIR} --project-dir {DBT_DIR} --no-partial-parse"
        ),
    )

    # ── Étape 3 : dbt test ──────────────────────────────
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"cd {DBT_DIR} && "
            f"{ENV_VARS} "
            f"dbt test --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}"
        ),
        # Si dbt test échoue (tests KO), le DAG est marqué FAILED
    )

    etl_warehouse >> dbt_run >> dbt_test

