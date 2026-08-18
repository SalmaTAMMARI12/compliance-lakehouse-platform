import pytest
from dgssi_platform.infrastructure.extraction.llm.texte_enrichi import (
    construire_texte_enrichi,
    extraire_section_synthese,
)


def test_construire_texte_enrichi():
    texte_markdown = "Introduction du rapport."
    tableaux = [
        [
            ["DNSSI- POL-RISQUE : Analyse de risque", "Valeur ignorée"],
            ["Constat: Absence d'analyse formelle", ""],
            ["Recommandation:", "Mettre en place une EBIOS"],
        ],
        [
            ["Notes d'audit : Le processus est en cours d'élaboration."],
        ]
    ]

    resultat = construire_texte_enrichi(texte_markdown, tableaux)

    assert "Introduction du rapport." in resultat
    assert "=== CONTENU DES TABLEAUX ===" in resultat
    assert "--- [DNSSI- POL-RISQUE : Analyse de risque] ---" in resultat
    assert "Constat : Absence d'analyse formelle" in resultat
    assert "Recommandation :\nMettre en place une EBIOS" in resultat
    assert "Notes d'audit : Le processus est en cours d'élaboration." in resultat


def test_extraire_section_synthese():
    texte_enrichi = (
        "Ceci est un long texte d'audit.\n"
        "Introduction... blah blah...\n"
        "Taux de conformité global : 76,70%\n"
        "Suite du rapport..."
    )

    section = extraire_section_synthese(texte_enrichi, max_longueur=100)
    assert "Taux de conformité global : 76,70%" in section


def test_extraire_section_synthese_fallback():
    texte_enrichi = "Un rapport très court sans mots clés."
    section = extraire_section_synthese(texte_enrichi, max_longueur=20)
    assert section == "Un rapport très cour"
