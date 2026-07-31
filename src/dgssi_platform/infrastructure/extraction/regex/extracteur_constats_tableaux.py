"""Extraction des non-conformités (constats + recommandations) depuis les
TABLEAUX du rapport DOCX d'audit organisationnel DNSSI.

Dans ce format, chaque tableau de mesure contient :
  - Cellule[0] : code de clause (ex. "POL-RISQUE : Analyse de risque")
  - Cellule[n] : "Constat:\n<texte du constat>"
  - Cellule[n+1] : "Recommandation:\n<texte de la recommandation>"

L'extraction est purement basée sur les tableaux, sans LLM ni regex de texte.
"""
from __future__ import annotations

import re

from dgssi_platform.domain.entities.non_conformite import NonConformite
from dgssi_platform.infrastructure.extraction.regex.extracteur_clauses_tableaux import (
    _PATTERN_CODE_CELLULE,
    _PREFIXE_VERS_CHAPITRE,
    _prefixe_du_code,
    _extraire_code,
)
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

_PATTERN_CONSTAT = re.compile(r"^Constat\s*:\s*", re.IGNORECASE)
_PATTERN_RECOMMANDATION = re.compile(r"^Recommandation\s*:\s*", re.IGNORECASE)

# Constats qui signalent une conformité (on les ignore)
_CONFORMES = {"ras", "conforme", "rас", "neant", "n/a", "na"}


def _est_conforme(texte: str) -> bool:
    return texte.strip().lower() in _CONFORMES or texte.strip().lower().startswith("conforme")


def _chapitre_du_code(code: str) -> str | None:
    prefixe = _prefixe_du_code(code)
    return _PREFIXE_VERS_CHAPITRE.get(prefixe) if prefixe else None


def extraire_non_conformites_depuis_tableaux(
    tableaux: list[list[list[str]]],
) -> tuple[list[NonConformite], float]:
    """Extrait les non-conformités en parcourant toutes les cellules des tableaux.

    Stratégie : on garde une fenêtre glissante (code_courant, recommandation_courante).
    Quand on rencontre un code de clause → on met à jour le chapitre courant.
    Quand on rencontre "Constat:" → on crée une NonConformite.
    Quand on rencontre "Recommandation:" → on l'attache au constat précédent (ou en file d'attente).
    """
    non_conformites: list[NonConformite] = []
    chapitre_courant: str = "Inconnu"
    code_courant: str = ""
    recommandation_en_attente: str | None = None

    for tableau in tableaux:
        for ligne in tableau:
            for cellule in ligne:
                texte = str(cellule).strip()
                if not texte:
                    continue

                # --- Détection d'un code de clause ---
                code = _extraire_code(texte)
                if code:
                    chapitre = _chapitre_du_code(code)
                    if chapitre:
                        chapitre_courant = chapitre
                        code_courant = code
                    continue

                # --- Détection d'un constat ---
                if _PATTERN_CONSTAT.match(texte):
                    corps = _PATTERN_CONSTAT.sub("", texte).strip()
                    if not corps or _est_conforme(corps):
                        continue
                    # Crée la non-conformité (la recommandation sera attachée plus tard)
                    nc = NonConformite(
                        chapitre=chapitre_courant,
                        texte_source=texte[:500],
                        resume_constat=corps[:500],
                        recommandation=None,
                        actifs_concernes=[code_courant] if code_courant else [],
                        echeance=None,
                        a_verifier=False,
                        est_note=False,
                    )
                    non_conformites.append(nc)
                    recommandation_en_attente = None
                    continue

                # --- Détection d'une recommandation ---
                if _PATTERN_RECOMMANDATION.match(texte):
                    corps = _PATTERN_RECOMMANDATION.sub("", texte).strip()
                    if corps.upper() in ("RAS", "N/A", "NA", ""):
                        continue
                    # Attache au dernier constat du même chapitre qui n'a pas encore de reco
                    for nc in reversed(non_conformites):
                        if nc.chapitre == chapitre_courant and nc.recommandation is None:
                            nc.recommandation = corps[:500]
                            break
                    continue

    nb = len(non_conformites)
    confiance = min(1.0, 0.5 + 0.05 * nb) if nb > 0 else 0.0
    logger.info(
        "Constats depuis tableaux : %d non-conformites extraites (confiance=%.2f)",
        nb, confiance,
    )
    return non_conformites, confiance
