"""Découpage d'un rapport DNSSI en chapitres, via les ancres de codes de
clauses. Logique unique, réutilisée par extracteur_clauses.py (codes) et
extracteur_constats.py (constats en texte libre pour le LLM), pour éviter
que les deux extracteurs divergent sur ce qui compte comme un vrai chapitre.
"""

from __future__ import annotations

import re

_PATTERN_ANCRE = re.compile(r"DNSSI\s*\(([^)]+)\)")
_PATTERN_CODE_VALIDE = re.compile(r"^[A-Z][A-Z0-9]*(\s*-\s*[A-Z0-9/]+)+$")


def _est_une_vraie_ancre(contenu_parentheses: str) -> bool:
    """Une vraie ancre de chapitre contient une liste de codes DNSSI
    (ex. 'POL-RISQUE, POL-FORMEL'), pas une phrase en français."""
    codes = [c.strip().rstrip(".") for c in contenu_parentheses.split(",")]
    codes = [c for c in codes if c]
    if not codes:
        return False
    nb_valides = sum(1 for c in codes if _PATTERN_CODE_VALIDE.match(c))
    return nb_valides / len(codes) >= 0.5


def trouver_ancres_chapitres(texte: str) -> list[re.Match]:
    """Liste ordonnée des vraies ancres de chapitre (Match objects, pour
    accéder à .start()/.end() et découper le texte autour)."""
    return [
        m for m in _PATTERN_ANCRE.finditer(texte)
        if _est_une_vraie_ancre(m.group(1))
    ]
