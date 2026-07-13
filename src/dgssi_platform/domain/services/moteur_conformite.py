"""Moteur de conformité — compare les données extraites d'un Audit à des
seuils réglementaires, produit des indicateurs exploitables.

Volontairement limité au niveau "KPI sur données déjà chiffrées" (taux
global, résultats techniques agrégés) — pas de croisement clause-par-clause
avec le référentiel DNSSI, qui nécessiterait l'extraction des 14 chapitres
(non faite à ce jour). Ce moteur reste 100% déterministe, aucune IA.
"""

from __future__ import annotations

from dgssi_platform.domain.entities.audit import Audit

SEUIL_CONFORMITE_ACCEPTABLE = 80.0  # seuil réglementaire indicatif, à faire valider par l'encadrant


def evaluer_conformite_globale(audit: Audit) -> dict[str, object]:
    """Statue si l'audit dépasse le seuil de conformité acceptable."""
    taux = audit.taux_conformite_global
    if taux is None:
        return {"statut": "INDETERMINE", "taux": None, "seuil": SEUIL_CONFORMITE_ACCEPTABLE}

    statut = "CONFORME" if taux >= SEUIL_CONFORMITE_ACCEPTABLE else "NON_CONFORME"
    return {"statut": statut, "taux": taux, "seuil": SEUIL_CONFORMITE_ACCEPTABLE}


def classer_elements_par_exposition(audit: Audit) -> list[dict[str, object]]:
    """Trie les équipements du plus au moins exposé, par score pondéré
    (les criticités élevées comptent plus que les faibles).
    """
    if not audit.audit_technique:
        return []

    ponderation = {"CRITIQUE": 4, "ELEVEE": 3, "MOYENNE": 2, "FAIBLE": 1}
    classement = []

    for element, valeurs in audit.audit_technique.resultats_par_element.items():
        score = sum(ponderation[niveau] * count for niveau, count in valeurs.items())
        classement.append({"element": element, "score_exposition": score, "detail": valeurs})

    return sorted(classement, key=lambda x: x["score_exposition"], reverse=True)


def compter_ecarts_critiques(audit: Audit) -> int:
    """Nombre total de constats CRITIQUE tous équipements confondus —
    KPI explicitement demandé par la fiche de stage."""
    if not audit.audit_technique:
        return 0
    return sum(
        valeurs["CRITIQUE"]
        for valeurs in audit.audit_technique.resultats_par_element.values()
    )