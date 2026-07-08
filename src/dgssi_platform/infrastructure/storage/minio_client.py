"""Client MinIO minimal — écrit des objets dans les zones bronze/silver/gold.
Utilise boto3 (API S3), MinIO étant compatible S3.
"""

from __future__ import annotations

import json
from typing import Any

import boto3

from dgssi_platform.shared.config import get_settings
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def _get_client():
    settings = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=f"http://{settings.minio_endpoint}",
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
    )


def upload_texte(bucket: str, cle: str, texte: str) -> None:
    client = _get_client()
    client.put_object(Bucket=bucket, Key=cle, Body=texte.encode("utf-8"))
    logger.info("Uploadé %s/%s (%d caractères)", bucket, cle, len(texte))


def upload_json(bucket: str, cle: str, donnees: Any) -> None:
    client = _get_client()
    contenu = json.dumps(donnees, ensure_ascii=False, indent=2)
    client.put_object(Bucket=bucket, Key=cle, Body=contenu.encode("utf-8"))
    logger.info("Uploadé %s/%s", bucket, cle)