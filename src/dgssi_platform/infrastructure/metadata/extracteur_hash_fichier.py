"""Calcule les métadonnées techniques d'un fichier local — hash SHA256, taille,
extension. Utilisé juste après le dépôt (avant tout parsing), pour garantir la
traçabilité dès l'entrée dans Bronze.

Volontairement une simple fonction, pas encore une classe implémentant un port
domaine (MetadataExtracteur) — on ajoutera cette abstraction seulement si un
jour on a plusieurs façons de calculer des métadonnées (ex. directement depuis
un objet S3 plutôt qu'un fichier local).
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from dgssi_platform.domain.entities.document_metadata import DocumentMetadata
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def calculer_metadata(chemin_fichier: Path) -> DocumentMetadata:
    """Lit le fichier une seule fois pour calculer son hash SHA256, par blocs
    de 8 Ko pour ne pas charger un gros PDF entièrement en mémoire.
    """
    hash_sha256 = hashlib.sha256()
    with chemin_fichier.open("rb") as f:
        for bloc in iter(lambda: f.read(8192), b""):
            hash_sha256.update(bloc)

    taille = chemin_fichier.stat().st_size
    logger.info("Métadonnées calculées pour %s (%d octets)", chemin_fichier.name, taille)

    return DocumentMetadata(
        chemin=str(chemin_fichier),
        nom_fichier=chemin_fichier.name,
        extension=chemin_fichier.suffix.lower(),
        taille_octets=taille,
        hash_sha256=hash_sha256.hexdigest(),
        date_reception=datetime.now(timezone.utc),
    )