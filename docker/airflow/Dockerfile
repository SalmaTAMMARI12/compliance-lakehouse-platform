FROM apache/airflow:2.10.5-python3.11

# ── Dépendances système ──────────────────────────────────
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    git \
    curl \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# ── Docker CLI (pour orchestrer les conteneurs frères) ────
# Permet à Airflow d'appeler `docker exec dgssi-worker ...`
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# ── Dépendances Python ───────────────────────────────────
# NOTE : PAS de sqlalchemy>=2.0 ici !
# Airflow fournit déjà SQLAlchemy 1.4.x en interne.
# L'extraction Docling (qui nécessite SQLAlchemy 2.x) tourne dans le conteneur worker isolé.
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
