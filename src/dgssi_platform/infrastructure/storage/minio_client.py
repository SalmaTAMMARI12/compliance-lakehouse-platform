"""Client MinIO minimal — écrit et lit des objets dans les zones bronze/silver/gold.
Utilise boto3 (API S3), MinIO étant compatible S3.
"""

from __future__ import annotations

import hashlib
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
    contenu = json.dumps(donnees, ensure_ascii=False, indent=2, default=str)
    client.put_object(Bucket=bucket, Key=cle, Body=contenu.encode("utf-8"))
    logger.info("Uploadé %s/%s", bucket, cle)


def telecharger_objet(bucket: str, cle: str) -> bytes:
    """Récupère le contenu brut (bytes) d'un objet MinIO. Nécessaire pour
    recalculer un hash ou relire un fichier déjà déposé.
    """
    client = _get_client()
    reponse = client.get_object(Bucket=bucket, Key=cle)
    contenu = reponse["Body"].read()
    logger.info("Téléchargé %s/%s (%d octets)", bucket, cle, len(contenu))
    return contenu


def telecharger_json(bucket: str, cle: str) -> Any:
    """Récupère et parse un objet JSON depuis MinIO (ex: le fichier de métadonnées)."""
    contenu = telecharger_objet(bucket, cle)
    return json.loads(contenu.decode("utf-8"))


def calculer_hash_sha256(contenu: bytes) -> str:
    """Calcule l'empreinte SHA-256 d'un contenu binaire."""
    return hashlib.sha256(contenu).hexdigest()


def verifier_integrite_fichier(bucket: str, nom_fichier: str) -> bool:
    """Recalcule le hash du fichier brut et le compare au hash stocké dans
    _metadata/{nom_fichier}.json (produit par NiFi au moment du dépôt).

    IMPORTANT : les clés ne doivent PAS être préfixées par le nom du bucket
    (ex. "bronze/") — le bucket est déjà passé séparément à boto3 via le
    paramètre `bucket`. Un préfixe en trop chercherait un sous-dossier
    inexistant à l'intérieur du bucket (bug corrigé le 13/07).

    Lève une ValueError si le fichier a été modifié depuis son dépôt.
    Retourne True si l'intégrité est confirmée.
    """
    cle_fichier = nom_fichier
    cle_metadata = f"_metadata/{nom_fichier}.json"

    contenu = telecharger_objet(bucket, cle_fichier)
    hash_actuel = calculer_hash_sha256(contenu)

    metadata = telecharger_json(bucket, cle_metadata)
    hash_stocke = metadata["content_SHA-256"]  # nom exact produit par NiFi (majuscules + tiret)

    if hash_actuel != hash_stocke:
        logger.error(
            "ALERTE INTÉGRITÉ sur %s : hash stocké=%s, hash recalculé=%s",
            nom_fichier, hash_stocke, hash_actuel,
        )
        raise ValueError(
            f"Intégrité compromise pour {nom_fichier} : "
            f"le fichier a changé depuis son dépôt dans bronze/."
        )

    logger.info("Intégrité confirmée pour %s (hash %s)", nom_fichier, hash_actuel)
    return True