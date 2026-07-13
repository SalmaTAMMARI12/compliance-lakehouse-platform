"""Validation de cohérence d'un Audit extrait — Data Quality, niveau domaine.

Complète le score de confiance (qui mesure "suis-je sûr d'avoir bien lu ?")
avec des règles de cohérence (qui vérifient "est-ce que ce que j'ai lu a un
sens ?"). Les deux sont complémentaires, pas redondants.
"""

from __future__ import annotations

from dgssi_platform.domain.entities.audit import Audit


def valider_audit(audit: Audit) -> list[str]:
    """Retourne la liste des erreurs de cohérence détectées (vide si valide)."""
    erreurs: list[str] = []

    if audit.taux_conformite_global is not None:
        if not (0 <= audit.taux_conformite_global <= 100):
            erreurs.append(
                f"Taux de conformité hors bornes [0,100]: {audit.taux_conformite_global}"
            )

    if not audit.historique_versions:
        erreurs.append("Aucune version dans l'historique — donnée suspecte")

    if audit.audit_technique:
        for element, valeurs in audit.audit_technique.resultats_par_element.items():
            for niveau, count in valeurs.items():
                if count < 0:
                    erreurs.append(f"{element}/{niveau}: valeur négative ({count})")

    if audit.classification == "INCONNUE":
        erreurs.append("Classification non extraite — vérification manuelle recommandée")

    return erreurs