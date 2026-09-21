# ═══════════════════════════════════════════════════════════
# Worker DGSSI — Conteneur d'extraction (SQLAlchemy 2.x)
# ═══════════════════════════════════════════════════════════
# Ce conteneur est isolé d'Airflow pour éviter le conflit
# SQLAlchemy 1.4 (Airflow) vs SQLAlchemy 2.x (notre ORM).
# Airflow l'appelle via `docker exec` pour orchestrer le pipeline complet.
# ═══════════════════════════════════════════════════════════
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       tesseract-ocr \
       git \
       libpq-dev \
       gcc \
       g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier le requirements du projet et remplacer psycopg2 par psycopg2-binary
# (évite de devoir compiler depuis les sources avec pg_config)
COPY requirements.txt /app/requirements.txt
RUN sed -i 's/^psycopg2==/psycopg2-binary==/' requirements.txt \
    && sed -i '/pywin32/d' requirements.txt \
    && pip install --no-cache-dir --timeout 300 -r requirements.txt

# Le projet est monté en volume, pas copié (pour refléter les changements en temps réel)
# Volume: .:/app dans docker-compose.yaml

# Le conteneur reste en veille, Airflow le réveille avec docker exec
CMD ["sleep", "infinity"]
