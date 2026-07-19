FROM apache/airflow:2.10.5-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*
USER airflow

RUN pip install --no-cache-dir --timeout 600 \
    psycopg2-binary \
    minio \
    pyyaml \
    python-dotenv
