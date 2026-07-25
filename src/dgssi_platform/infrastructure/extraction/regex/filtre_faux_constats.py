"""Filtre structurel pour identifier les faux constats d'écart.
Certaines lignes capturées par le parseur sous le titre "Constats" sont
en réalité des titres de documents, des mots-clés d'entretien ou des
notes d'audit positives (mélangées par Docling).
"""

from __future__ import annotations

import re

# Mots-clés indiquant qu'il s'agit d'une preuve/document
_MOTS_CLEFS_PREUVES = {
    "interview", "entretien", "extrait de", "exemple de", "capture d'écran",
    "version", "v1", "v2", "v3",
}

# Verbes/expressions typiques d'un constat d'écart (négatif/restrictif)
_MARQUEURS_ECART = [
    "n'est pas", "ne sont pas", "ne dispose pas", "absence de", "aucun",
    "aucune", "non conforme", "ne couvre pas", "en cours de", "pas encore",
    "pas validé", "non validé", "incomplet", "défaut de", "manque de"
]

_PATTERN_DATE_PARENTHESES = re.compile(r"\([a-zA-Zéû]+\s+\d{4}\)") # Ex: (Juin 2023)

def _nettoyer_ligne(ligne: str) -> str:
    # Retire les tirets, puces, et espaces de début
    return ligne.lstrip("- •o\t ").strip()

def est_probable_faux_constat(ligne: str) -> bool:
    """Retourne True si la ligne ressemble structurellement à une preuve,
    un titre de document, ou une note d'audit plutôt qu'à un constat d'écart.
    """
    ligne_nettoyee = _nettoyer_ligne(ligne)
    if not ligne_nettoyee:
        return True # Ligne vide

    ligne_lower = ligne_nettoyee.lower()
    mots = [m for m in ligne_lower.split() if m.isalnum()]

    # 1. Très court et sans marqueur d'écart
    if len(mots) < 8 and not any(m in ligne_lower for m in _MARQUEURS_ECART):
        return True

    # 2. Ressemble à un titre de document ou méthode de collecte
    if any(m in ligne_lower for m in _MOTS_CLEFS_PREUVES):
        return True
    
    if _PATTERN_DATE_PARENTHESES.search(ligne_nettoyee):
        return True
        
    # Un titre commence souvent par une majuscule et n'a pas de point final
    if ligne_nettoyee[0].isupper() and not ligne_nettoyee.endswith(".") and len(mots) < 12 and not any(m in ligne_lower for m in _MARQUEURS_ECART):
        return True

    return False
