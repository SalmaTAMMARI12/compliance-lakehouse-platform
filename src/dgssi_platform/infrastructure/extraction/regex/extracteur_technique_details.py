"""Extraction des referentiels utilises (§4.3) et des vulnerabilites /
points d'amelioration technique (§4.5.d), qui detaillent en texte
structure ce que le tableau chiffre resultats_par_element compte
seulement en nombre (CRITIQUE/ELEVEE/MOYENNE/FAIBLE par equipement).
Regex pur : les 3 categories du §4.5.d sont sous des en-tetes fixes,
suivies de puces simples — pas besoin de LLM ici.
"""

from __future__ import annotations

import re

_PATTERN_PUCE = re.compile(r"^-\s*(.+?)\s*;?\s*$")

_CATEGORIES_VULNERABILITES = [
    ("equipements_reseau", "Les équipements de sécurité et du réseau :"),
    ("serveur_messagerie", "Le serveur de messagerie :"),
    ("serveur_web", "Le serveur web :"),
]


def _extraire_puces_entre(texte: str, debut: str, fin: str | None) -> list[str]:
    idx_debut = texte.find(debut)
    if idx_debut == -1:
        return []
    idx_fin = texte.find(fin, idx_debut + len(debut)) if fin else len(texte)
    if idx_fin == -1:
        idx_fin = idx_debut + 3000  # borne de securite
    section = texte[idx_debut:idx_fin]

    resultats = []
    for ligne in section.split("\n"):
        m = _PATTERN_PUCE.match(ligne.strip())
        if m:
            resultats.append(m.group(1).strip())
    return resultats


def extraire_referentiels_utilises(texte: str) -> tuple[list[str], float]:
    """Referentiels techniques cites en §4.3 (ex. CIS Benchmarks, DISA STIGs)."""
    elements = _extraire_puces_entre(texte, "4.3 Référentiels utilisés", "4.4 Echelle")
    confiance = 1.0 if elements else 0.0
    return elements, confiance


def extraire_vulnerabilites_par_categorie(texte: str) -> tuple[dict[str, list[str]], float]:
    """Points d'amelioration/vulnerabilites du §4.5.d, groupes par les 3
    categories nommees explicitement dans le rapport (equipements reseau,
    serveur de messagerie, serveur web)."""
    resultat: dict[str, list[str]] = {}

    for cle, marqueur_debut in _CATEGORIES_VULNERABILITES:
        idx_position = [c for c, m in _CATEGORIES_VULNERABILITES].index(cle)
        marqueur_fin = (
            _CATEGORIES_VULNERABILITES[idx_position + 1][1]
            if idx_position + 1 < len(_CATEGORIES_VULNERABILITES)
            else None
        )
        elements = _extraire_puces_entre(texte, marqueur_debut, marqueur_fin)
        resultat[cle] = elements

    nb_total = sum(len(v) for v in resultat.values())
    confiance = 1.0 if nb_total > 0 else 0.0
    return resultat, confiance
