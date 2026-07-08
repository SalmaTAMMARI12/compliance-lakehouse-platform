"""Tests golden — valeurs figées, vérifiées sur le rapport PASSI de référence
(page 2 : bloc métadonnées et historique des versions)."""

from __future__ import annotations

import pytest

from dgssi_platform.infrastructure.extraction.regex.extracteur_metadonnees import (
    extraire_classification,
    extraire_historique_versions,
)

TABLEAU_METADONNEES = [
    ["Auteur", "AAAAAAAAA"],
    ["Classification", "Confidentiel"],
    ["Titre du document", "Audit de sécurité des systèmes d'information..."],
    ["Type de document", "Rapport d'audit"],
]

TABLEAU_HISTORIQUE = [
    ["V1.0", "Version initiale", "15/11/2023", "AAAAAAAAA"],
    ["V1.1", "Modifiée et partagée avec l'auditer", "09/02/2024", "AAAAAAAAA"],
    ["V 1.2", "Intègre les remarques de l'Auditer", "02/05/2024", "AAAAAAAAA"],
]


def test_extraire_classification_golden() -> None:
    tableaux = [TABLEAU_METADONNEES]
    classification, confiance = extraire_classification(tableaux)

    assert classification == "Confidentiel"
    assert confiance == 1.0


def test_extraire_classification_absente() -> None:
    tableaux = [[["Un tableau", "sans classification"]]]
    classification, confiance = extraire_classification(tableaux)

    assert classification is None
    assert confiance == 0.0


def test_extraire_historique_versions_golden() -> None:
    tableaux = [TABLEAU_HISTORIQUE]
    versions, confiance = extraire_historique_versions(tableaux)

    assert len(versions) == 3
    assert versions[0]["version"] == "V1.0"
    assert versions[0]["date"] == "15/11/2023"
    assert versions[2]["version"] == "V 1.2"  # espace conservé tel quel dans le PDF source
    assert confiance == pytest.approx(0.9)


def test_extraire_historique_versions_absent() -> None:
    tableaux = [[["Pas de version ici", "juste du texte"]]]
    versions, confiance = extraire_historique_versions(tableaux)

    assert versions == []
    assert confiance < 0.5