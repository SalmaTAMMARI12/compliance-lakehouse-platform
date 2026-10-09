FROM apache/airflow:2.10.5-python3.11
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    git \
    curl \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

USER airflow
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
