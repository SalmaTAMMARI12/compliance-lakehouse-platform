"""Extraction du total officiel d'ecarts et de leur repartition par type,
depuis la phrase de synthese du rapport (ex. section 2.3 : "L'audit a
permis de relever 19 fiches d'ecarts dont 11 significatif, 07 non
significatifs et une remarque."). Regex sur une phrase au motif stable —
pas de classification par constat individuel : cette information n'existe
pas a ce niveau de granularite dans le rapport source (voir le commentaire
dans non_conformite.py sur la suppression du champ 'type').
"""

from __future__ import annotations

import re

_MOTS_NOMBRES = {
    "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
    "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10,
}

# Docling insere parfois un espace parasite a l'interieur d'un nombre
# (ex. "1 1" au lieu de "11") — tolere par \d[\d ]*\d|\d au lieu de \d+.
_NOMBRE = r"\d(?:[\s]?\d)*"

# \s+ (un ou plusieurs) partout, jamais \s seul — Docling produit un
# nombre variable d'espaces selon le rapport source. "non[\s-]+" tolere
# aussi bien "non significatif" que "non-significatif".
_PATTERN = re.compile(
    rf"({_NOMBRE})\s+fiches?\s+d[\s']*[ée]carts?\s+dont\s+"
    rf"({_NOMBRE})\s+significatifs?,?\s+"
    rf"({_NOMBRE}|\w+)\s+non[\s-]+significatifs?\s+et\s+"
    rf"({_NOMBRE}|\w+)\s+remarques?",
    re.IGNORECASE,
)


def _vers_nombre(texte: str) -> int:
    texte = texte.strip().lower()
    texte_sans_espaces = texte.replace(" ", "")
    if texte_sans_espaces.isdigit():
        return int(texte_sans_espaces)
    return _MOTS_NOMBRES.get(texte, 0)


def extraire_totaux_ecarts(texte: str) -> tuple[dict[str, int], float]:
    """Retourne ({"significatif": .., "non_significatif": .., "remarque": ..}, confiance).
    Confiance = 1.0 si la somme des 3 categories correspond au total annonce
    (auto-verification de coherence), 0.6 sinon, 0.0 si phrase introuvable."""
    match = _PATTERN.search(texte)
    if not match:
        return {}, 0.0

    total, significatif, non_significatif, remarque = match.groups()
    resultat = {
        "significatif": _vers_nombre(significatif),
        "non_significatif": _vers_nombre(non_significatif),
        "remarque": _vers_nombre(remarque),
    }
    total_annonce = int(total)
    coherent = sum(resultat.values()) == total_annonce
    return resultat, (1.0 if coherent else 0.6)
