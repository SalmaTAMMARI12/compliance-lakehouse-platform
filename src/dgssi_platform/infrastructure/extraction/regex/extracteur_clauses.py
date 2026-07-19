"""Extraction des codes de clauses DNSSI, indépendamment de la détection de
titres Markdown par Docling (peu fiable : §3.4 "Gestion des actifs
informationnels" n'est pas reconnue comme un titre, et son contenu se
retrouve rattaché au chapitre précédent si on se base sur les titres).

Approche robuste : on cherche TOUTES les occurrences de "DNSSI (...)" dans
le texte entier, filtrées pour ne garder que celles qui ressemblent
réellement à une liste de codes. Le rapport suit toujours l'ordre §3.1 à
§3.14 sans exception, donc l'ordre d'apparition suffit à associer chaque
groupe trouvé au bon chapitre.

Tolérance de forme : Docling introduit deux artefacts liés aux retours à
la ligne du PDF source : (a) un tiret perdu (EXP-PROC-CAP -> EXPPROC-CAP)
et (b) un espace parasite autour d'un tiret (PHYS-ZONE-EAU ->
PHYS-ZONE -EAU ou PHYS- MAT-CABL). Le regex de validation tolère les deux.
"""
from __future__ import annotations

import re
import warnings

_PATTERN_CLAUSES = re.compile(r"DNSSI\s*\(([^)]+)\)")
# Tolère un espace optionnel de part et d'autre de chaque tiret
# (artefact Docling), en plus des tirets normaux.
_PATTERN_CODE_VALIDE = re.compile(r"^[A-Z][A-Z0-9]*(\s*-\s*[A-Z0-9/]+)+$")


def _nettoyer_code(code: str) -> str:
    return code.strip().rstrip(".").strip()


def _codes_semblent_valides(codes: list[str]) -> bool:
    """Un vrai groupe de clauses DNSSI est fait de codes du type
    'POL-RISQUE' ou 'ACC-UTILIS-IDF/AUTH' — filtre les faux positifs
    (mentions isolées de DNSSI, ex. dans un intitulé de tableau)."""
    if not codes:
        return False
    nb_valides = sum(1 for c in codes if _PATTERN_CODE_VALIDE.match(c))
    return nb_valides / len(codes) >= 0.5


def extraire_groupes_clauses(texte: str) -> list[list[str]]:
    """Liste ordonnée des groupes de codes valides trouvés dans le texte."""
    groupes = []
    for match in _PATTERN_CLAUSES.finditer(texte):
        codes = [_nettoyer_code(c) for c in match.group(1).split(",")]
        codes = [c for c in codes if c]
        if _codes_semblent_valides(codes):
            groupes.append(codes)
    return groupes


def extraire_clauses_par_chapitre(
    texte: str, noms_chapitres_ordonnes: list[str]
) -> tuple[dict[str, list[str]], float]:
    """Associe chaque groupe de codes trouvé, dans l'ordre d'apparition, au
    chapitre correspondant de noms_chapitres_ordonnes."""
    groupes = extraire_groupes_clauses(texte)

    if len(groupes) != len(noms_chapitres_ordonnes):
        warnings.warn(
            f"{len(groupes)} groupes de clauses trouvés pour "
            f"{len(noms_chapitres_ordonnes)} chapitres attendus — "
            "l'association ordre-par-ordre peut être décalée, à vérifier."
        )

    resultats = dict(zip(noms_chapitres_ordonnes, groupes))
    confiance = (
        min(len(groupes), len(noms_chapitres_ordonnes)) / len(noms_chapitres_ordonnes)
        if noms_chapitres_ordonnes else 0.0
    )
    return resultats, confiance