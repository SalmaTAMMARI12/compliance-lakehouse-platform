"""Script : lit texte.md et tableaux.json depuis Silver (MinIO), applique
ExtracteurHybride, affiche l'Audit résultant. Complète le pipeline manuel
qu'on avait laissé en deux morceaux (parser_vers_silver.py écrit dans
Silver, celui-ci lit depuis Silver) — pas encore automatisé en un seul
flux (Airflow le fera plus tard), mais connecté à MinIO pour de vrai.
"""

from __future__ import annotations

import json
import sys

import boto3

from dgssi_platform.domain.interfaces.parseur import DocumentBrut
from dgssi_platform.infrastructure.extraction.extracteur_hybride import ExtracteurHybride
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


def lire_texte(bucket: str, cle: str) -> str:
    client = _get_client()
    obj = client.get_object(Bucket=bucket, Key=cle)
    return obj["Body"].read().decode("utf-8")


def lire_json(bucket: str, cle: str):
    return json.loads(lire_texte(bucket, cle))


def extraire_depuis_silver(nom_document: str) -> None:
    prefixe = f"{nom_document}/"
    texte = lire_texte("silver", f"{prefixe}texte.md")
    tableaux = lire_json("silver", f"{prefixe}tableaux.json")

    document = DocumentBrut(texte=texte, tableaux=tableaux, nb_pages=None)
    audit = ExtracteurHybride().extraire(document)

    print("Prestataire:", audit.prestataire_audit)
    print("Classification:", audit.classification)
    print("Taux global:", audit.taux_conformite_global)
    print("Nb versions historique:", len(audit.historique_versions))
    if audit.audit_technique:
        print("Nb équipements:", len(audit.audit_technique.resultats_par_element))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extraire_audit_depuis_silver.py <nom_document>")
        sys.exit(1)

    extraire_depuis_silver(sys.argv[1])