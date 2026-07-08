"""Entité DocumentMetadata — capturée pour CHAQUE fichier dès son entrée en Bronze,
avant tout parsing. Indépendante du contenu métier : elle ne sait pas si c'est un
audit DNSSI ou un dossier d'homologation, juste des faits techniques sur le fichier.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class StatutPipeline(StrEnum):
    RECU = "recu"                          # déposé, hash calculé, pas encore lu
    PARSE = "parse"                        # texte/tableaux extraits (Docling)
    EXTRAIT = "extrait"                    # champs métier identifiés
    VALIDE = "valide"                      # passé les contrôles de cohérence
    CONFORME_CALCULE = "conforme_calcule"  # KPIs de conformité calculés
    ECHEC = "echec"                        # bloqué à une étape, avec raison


class DocumentMetadata(BaseModel):
    chemin: str                 # ex. "bronze/Exemple de rapport d'audit.pdf"
    nom_fichier: str
    extension: str
    taille_octets: int
    hash_sha256: str
    date_reception: datetime
    statut: StatutPipeline = StatutPipeline.RECU
    message_erreur: str | None = None   # rempli seulement si statut == ECHEC