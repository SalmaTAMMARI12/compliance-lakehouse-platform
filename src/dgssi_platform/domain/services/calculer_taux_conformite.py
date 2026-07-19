"""calculer_taux_conformite.py — calcule un taux de couverture réel en
croisant le référentiel DNSSI (104 codes de clauses attendus) avec ce
qu'un audit donné déclare avoir couvert, chapitre par chapitre.

Comparaison normalisée (tirets ignorés) : Docling perd occasionnellement des
tirets aux retours à la ligne du PDF source lors de la conversion en
Markdown (ex. "EXP-PROC-CAP" devient "EXPPROC-CAP"). Comparer sans tiret
absorbe cet artefact sans avoir à corriger chaque cas individuellement.
"""
from __future__ import annotations

from dgssi_platform.domain.entities.audit import Audit
from dgssi_platform.domain.entities.exigence import Exigence


def _normaliser(code: str) -> str:
    # Ignore tirets ET espaces parasites (artefacts Docling), ex.
    # "PHYS-ZONE -EAU" et "PHYS-ZONE-EAU" doivent matcher le même code.
    return code.upper().replace("-", "").replace(" ", "").strip()


def calculer_couverture_referentiel(audit: Audit, exigences: list[Exigence]) -> dict[str, object]:
    codes_couverts_normalises = {
        _normaliser(code)
        for chapitre in audit.chapitres
        for code in chapitre.clauses
    }

    codes_manquants = [
        e.code for e in exigences
        if _normaliser(e.code) not in codes_couverts_normalises
    ]
    nb_couverts = len(exigences) - len(codes_manquants)
    taux_couverture = 100 * nb_couverts / len(exigences) if exigences else 0.0

    return {
        "taux_couverture_referentiel": round(taux_couverture, 2),
        "nb_exigences_attendues": len(exigences),
        "nb_exigences_couvertes": nb_couverts,
        "codes_manquants": sorted(codes_manquants),
    }