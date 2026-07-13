"""Persiste les résultats du moteur de conformité en base."""

from __future__ import annotations

from dgssi_platform.infrastructure.database.models.audit_model import (
    EvaluationConformiteModel,
)
from dgssi_platform.infrastructure.database.session import get_session


def sauvegarder_evaluation(
    audit_id: int,
    statut: str,
    seuil: float,
    nb_ecarts_critiques: int,
    element_le_plus_expose: str,
) -> int:
    with get_session() as session:
        modele = EvaluationConformiteModel(
            audit_id=audit_id,
            statut=statut,
            seuil_applique=seuil,
            nb_ecarts_critiques=nb_ecarts_critiques,
            element_le_plus_expose=element_le_plus_expose,
        )
        session.add(modele)
        session.commit()
        return modele.id