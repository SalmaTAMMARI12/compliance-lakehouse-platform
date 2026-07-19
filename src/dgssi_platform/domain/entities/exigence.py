"""Entité Exigence — une clause du référentiel DNSSI, telle que définie par
l'autorité nationale (indépendante de tout audit).

À distinguer de ChapitreAudit (domain/entities/audit.py) : ChapitreAudit
représente ce qu'UN audit a constaté pour un chapitre donné ; Exigence
représente ce que LE référentiel exige, point de comparaison fixe pour
calculer une couverture. Chargée depuis infrastructure/referentiel/seeds/dnssi_v2.yaml
via infrastructure/referentiel/loader.py — cette entité est la version
"objet métier" de ces données, pas une nouvelle source de vérité.
"""

from __future__ import annotations

from pydantic import BaseModel


class Exigence(BaseModel):
    code: str                      # ex. "POL-RISQUE" — identifiant du référentiel DNSSI
    chapitre: str                  # ex. "Politique de sécurité des systèmes d'information"
    objectif: str
    points_de_controle: list[str] = []