"""Extraction du perimetre fonctionnel (section 1.1, systemes concernes par
l'audit de conformite DNSSI) et du perimetre technique (section 4.1,
equipements concernes par l'audit technique). Deux perimetres distincts
dans le rapport, deux champs distincts dans le modele (Audit.perimetre_fonctionnel
et AuditTechnique.perimetre_technique).
"""

from __future__ import annotations

import re

_PATTERN_PUCE = re.compile(r"^[\-\u2022\*]\s*(.+?)\s*;?\s*$")


def _extraire_puces_entre(texte: str, debut_marqueur: str, fin_marqueur: str) -> list[str]:
    # rfind plutot que find : la table des matieres (debut du document)
    # contient aussi ce marqueur, avant le vrai contenu.
    idx_debut = texte.rfind(debut_marqueur)
    if idx_debut == -1:
        return []
    idx_fin = texte.find(fin_marqueur, idx_debut + len(debut_marqueur))
    if idx_fin == -1:
        idx_fin = idx_debut + 2000  # borne de securite si le marqueur de fin est introuvable
    section = texte[idx_debut:idx_fin]

    resultats = []
    for ligne in section.split("\n"):
        m = _PATTERN_PUCE.match(ligne.strip())
        if m:
            resultats.append(m.group(1).strip())
    return resultats


def extraire_perimetre_fonctionnel(texte: str) -> tuple[list[str], float]:
    """Systemes concernes par l'audit de conformite DNSSI (section 1.1)."""
    elements = _extraire_puces_entre(
        texte, "Périmètre de l", "Déroulement de l"
    )
    confiance = 1.0 if elements else 0.0
    return elements, confiance


def extraire_perimetre_technique(texte: str) -> tuple[list[str], float]:
    """Equipements concernes par l'audit technique (section 4.1)."""
    elements = _extraire_puces_entre(
        texte, "4.1 Périmètre", "4.2 Objectif"
    )
    confiance = 1.0 if elements else 0.0
    return elements, confiance
