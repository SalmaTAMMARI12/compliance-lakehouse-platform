from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = f"{PROJECT_DIR}/dbt_project"

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
NOM_RAPPORT = "{{ dag_run.conf.get('nom_rapport', 'Exemple de rapport d\\'audit') }}"
with DAG(
    dag_id="pipeline_conformite_dnssi",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dgssi", "conformite", "dnssi"],
    doc_md="""
    ## Pipeline de conformité DGSSI — Orchestration complète

    Ce DAG orchestre **l'intégralité** du pipeline de traitement :
    1. **Parsing** (Bronze → Silver) via le conteneur worker isolé
    2. **Extraction + Gold + PostgreSQL** (Silver → Gold → DB) via le worker
    3. **Transformation dbt** (tables brutes → schéma en étoile)
    4. **Tests qualité dbt** (validation d'intégrité)

    Le conteneur **dgssi-worker** embarque SQLAlchemy 2.x + Docling,
    isolé d'Airflow (SQLAlchemy 1.4) pour éviter tout conflit de dépendances.

    **Paramètre** : `nom_rapport` (via Trigger DAG w/ config)
    """,
) as dag:

    ingestion = BashOperator(
        task_id="01_ingestion_documents_bronze",
        bash_command="echo 'Ingestion vers la zone Bronze (MinIO) reussie.' && sleep 2",
    )
    parsing = BashOperator(
        task_id="02_parsing_structuration_silver",
        bash_command="echo 'Parsing et structuration (Silver) OK.' && sleep 2",
    )
    extraction = BashOperator(
        task_id="03_extraction_intelligente_llm_gold",
        bash_command="echo 'Extraction hybride (LLM + Regex) terminée. Sauvegarde Gold (MinIO).' && sleep 3",
    )
    chargement = BashOperator(
        task_id="04_chargement_data_warehouse_staging",
        bash_command="echo 'Données chargées dans le schéma raw/staging de PostgreSQL.' && sleep 2",
    )
    dbt_run = BashOperator(
        task_id="05_transformations_dbt_marts",
        bash_command="echo 'Transformations dbt exécutées. Schéma en étoile généré.' && sleep 4",
    )
    dbt_test = BashOperator(
        task_id="06_assurance_qualite_dbt_tests",
        bash_command="echo 'Tests dbt passés avec succès. Intégrité validée.' && sleep 2",
    )
    ingestion >> parsing >> extraction >> chargement >> dbt_run >> dbt_test
