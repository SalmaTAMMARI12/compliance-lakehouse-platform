"""Entité IIV — Infrastructure d'Importance Vitale.

Nom et secteur NON extractibles du rapport (document anonymisé, page 1 :
"XXXXXXXXXX"). Valeurs saisies manuellement pour ce rapport précis, le temps
de construire le pipeline de bout en bout. Pas de mécanisme de déduction
automatique tant qu'aucune source réelle n'est confirmée.
"""

from __future__ import annotations

from pydantic import BaseModel


class IIV(BaseModel):
    nom: str
    secteur: str