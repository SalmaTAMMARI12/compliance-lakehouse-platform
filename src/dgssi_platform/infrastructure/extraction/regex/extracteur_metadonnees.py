"""Extracteur regex pour les métadonnées du document (page 2 du rapport PASSI).

Deux formes détectées : un tableau clé-valeur (Auteur, Classification...) et
un tableau à 4 colonnes régulières (historique des versions). Détection par
structure, jamais par position — même principe que extracteur_tableaux_chiffres.
"""

from __future__ import annotations

import re

from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

_SEUIL_CONFIANCE_MINIMAL = 0.5
# V optionnel : "V1.0", "V 1.2" ET "1.0", "2.0" sont tous valides
_MOTIF_VERSION = re.compile(r"^V?\s?\d+\.\d+$")


def extraire_classification(tableaux: list[list[list[str]]]) -> tuple[str | None, float]:
    """Cherche une ligne ['Classification', <valeur>] dans un tableau clé-valeur."""
    for tableau in tableaux:
        for ligne in tableau:
            if len(ligne) == 2 and ligne[0].strip() == "Classification":
                valeur = ligne[1].strip()
                if valeur:
                    return valeur, 1.0

    logger.warning("Classification introuvable")
    return None, 0.0


def extraire_historique_versions(
    tableaux: list[list[list[str]]],
) -> tuple[list[dict[str, str]], float]:
    """Un tableau est candidat s'il a au moins une ligne à 4 colonnes dont la
    première matche le motif de version (ex. 'V1.0', 'V 1.2').
    """
    meilleur_score = 0.0
    meilleures_versions: list[dict[str, str]] = []

    for tableau in tableaux:
        versions: list[dict[str, str]] = []
        for ligne in tableau:
            # Format 4 colonnes (rapport PDF référence) : version, commentaire, date, auteur
            if len(ligne) == 4:
                version, commentaire, date, auteur = ligne
                if not _MOTIF_VERSION.match(version.strip()):
                    continue
                versions.append({
                    "version": version.strip(),
                    "commentaire": commentaire.strip(),
                    "date": date.strip(),
                    "auteur": auteur.strip(),
                })
            # Format 3 colonnes (rapport DOCX) : version, auteur, commentaire
            elif len(ligne) == 3:
                version, auteur, commentaire = ligne
                if not _MOTIF_VERSION.match(version.strip()):
                    continue
                versions.append({
                    "version": version.strip(),
                    "commentaire": commentaire.strip(),
                    "date": "",  # non disponible dans ce format
                    "auteur": auteur.strip(),
                })

        if not versions:
            continue

        score = min(1.0, 0.3 + 0.2 * len(versions))
        if score > meilleur_score:
            meilleur_score = score
            meilleures_versions = versions

    if meilleur_score < _SEUIL_CONFIANCE_MINIMAL:
        logger.warning("Historique des versions introuvable ou peu fiable")
        return [], meilleur_score

    return meilleures_versions, meilleur_score