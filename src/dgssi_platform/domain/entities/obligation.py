"""Entités du référentiel légal (loi 05-20 / décret 2-21-406) — distinctes
des Exigence DNSSI : ce sont des obligations réglementaires avec périodicité,
pas des clauses techniques vérifiables par contrôle.
Chargées depuis infrastructure/referentiel/seeds/referentiel_legal.yaml.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class SecteurIIV(StrEnum):
    """Les 15 secteurs de l'Annexe 1 du décret 2-21-406. Remplace le texte
    libre encore utilisé dans IIV.secteur (voir iiv.py) une fois qu'une
    source réelle de classification sectorielle existe (déduction depuis le
    rapport, ou saisie manuelle contrainte à cette liste)."""

    SECURITE_PUBLIQUE = "securite_publique"
    AFFAIRES_ETRANGERES = "affaires_etrangeres"
    FINANCES = "finances"
    LEGISLATION = "legislation"
    AGRICULTURE = "agriculture"
    SANTE = "sante"
    INDUSTRIE_COMMERCE_NUMERIQUE = "industrie_commerce_numerique"
    COMMUNICATION_AUDIOVISUELLE = "communication_audiovisuelle"
    ENERGIE = "energie"
    MINES = "mines"
    TRANSPORTS = "transports"
    EAU = "eau"
    BANCAIRE = "bancaire"
    TELECOMMUNICATIONS = "telecommunications"
    ASSURANCES = "assurances"


class Obligation(BaseModel):
    code: str                              # ex. "OBLIG-REVU-CLASSIF"
    description: str
    texte_reference: str                   # ex. "decret_2_21_406"
    article: str | None = None
    type_audit_requis: str | None = None
    periodicite_mois: int | None = None    # ex. 36 pour révision classification (art. 15)