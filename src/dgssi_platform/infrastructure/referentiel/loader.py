"""Charge le référentiel DNSSI depuis le fichier YAML statique.

Donnée réglementaire stable — chargée une fois, jamais extraite d'un rapport
individuel (cohérent avec la distinction actée : le contenu réglementaire est
fixe par la loi, seule la mise en forme d'un rapport varie).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_CHEMIN_REFERENTIEL = Path(__file__).parent / "seeds" / "dnssi_v2.yaml"


@lru_cache
def charger_referentiel_dnssi() -> dict[str, Any]:
    with _CHEMIN_REFERENTIEL.open(encoding="utf-8") as f:
        return yaml.safe_load(f)