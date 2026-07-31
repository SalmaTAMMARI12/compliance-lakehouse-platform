"""Extracteur regex sur le TEXTE LIBRE (pas les tableaux) — cas différent des
autres extracteurs de cette famille, qui ne lisaient jusqu'ici que
document.tableaux. Le prestataire d'audit n'apparaît que dans une phrase de
prose (page 4 du rapport de référence), jamais dans un tableau.
"""

from __future__ import annotations

import re

from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

# Motif observé page 4 : "Le PASSI FFFFFF a procédé à un audit de la sécurité..."
# Capture non gourmande : tout ce qui suit "Le " jusqu'à " a procédé"
_MOTIF_PRESTATAIRE = re.compile(r"Le\s+(.+?)\s+a procédé")


def extraire_prestataire(texte: str) -> tuple[str | None, float]:
    match = _MOTIF_PRESTATAIRE.search(texte)
    if not match:
        logger.warning("Prestataire d'audit introuvable dans le texte")
        return None, 0.0

    prestataire = match.group(1).strip()
    
    # Rejet des termes génériques
    termes_generiques = ["cabinet d'audit", "prestataire", "l'auditeur", "passi", "cabinet médical", "cabinet", "expert"]
    if prestataire.lower() in termes_generiques:
        logger.warning(f"Prestataire rejeté car trop générique : {prestataire}")
        return None, 0.0

    # Confiance réduite si le résultat est suspicieusement long
    # le motif a probablement capturé plus qu'un simple nom de prestataire
    # (ex. si "a procédé" apparaît ailleurs dans une autre phrase du document).
    confiance = 0.9 if len(prestataire) < 40 else 0.4

    return prestataire, confiance