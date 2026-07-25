FROM apache/airflow:2.10.5-python3.11

# ── Dépendances système ──────────────────────────────────
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        git \
    && rm -rf /var/lib/apt/lists/*
USER airflow

# ── Dépendances Python ───────────────────────────────────
# NOTE : PAS de sqlalchemy>=2.0 ici !
# Airflow fournit déjà SQLAlchemy 1.4.x en interne.
# Les scripts ETL (etl_vers_warehouse.py) utilisent psycopg2 directement.
# L'extraction Docling (qui nécessite SQLAlchemy 2.x) tourne en local, hors Airflow.
RUN pip install --no-cache-dir --timeout 300 \
    psycopg2-binary \
    minio \
    boto3 \
    pyyaml \
    python-dotenv \
    pydantic \
    pydantic-settings \
    "dbt-core>=1.8.0,<2.0.0" \
    "dbt-postgres>=1.8.0,<2.0.0"
