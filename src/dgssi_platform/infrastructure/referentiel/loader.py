"""Charge le référentiel DNSSI et le référentiel légal (loi/décret) depuis
les fichiers YAML statiques.
Donnée réglementaire stable — chargée une fois, jamais extraite d'un rapport
individuel (cohérent avec la distinction actée : le contenu réglementaire est
fixe par la loi, seule la mise en forme d'un rapport varie).
"""
from __future__ import annotations
from dgssi_platform.domain.entities.exigence import Exigence
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_CHEMIN_REFERENTIEL_DNSSI = Path(__file__).parent / "seeds" / "dnssi_v2.yaml"
_CHEMIN_REFERENTIEL_LEGAL = Path(__file__).parent / "seeds" / "referentiel_legal.yaml"


@lru_cache
def charger_referentiel_dnssi() -> dict[str, Any]:
    with _CHEMIN_REFERENTIEL_DNSSI.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache
def charger_referentiel_legal() -> dict[str, Any]:
    with _CHEMIN_REFERENTIEL_LEGAL.open(encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def obtenir_exigences() -> list[Exigence]:                     # ← nouvelle fonction
    """Aplatit dnssi_v2.yaml (chapitres → codes_clauses) en liste d'Exigence,
    une par code de clause DNSSI."""
    referentiel = charger_referentiel_dnssi()
    exigences = []
    for chapitre in referentiel["chapitres"]:
        for code in chapitre.get("codes_clauses", []):
            exigences.append(
                Exigence(
                    code=code,
                    chapitre=chapitre["nom"],
                    objectif="",
                )
            )
    return exigences
def obtenir_noms_chapitres_ordonnes() -> list[str]:
    referentiel = charger_referentiel_dnssi()
    chapitres_tries = sorted(referentiel["chapitres"], key=lambda c: c["numero"])
    return [c["nom"] for c in chapitres_tries]