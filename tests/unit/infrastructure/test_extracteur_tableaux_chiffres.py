"""Tests golden — valeurs figées, vérifiées à la main sur le rapport PASSI
de référence (pages 9-10 pour le taux global, page 37 pour les résultats
par élément). Si ces tests cassent après une modification du regex, c'est
une régression réelle, pas un faux positif à ignorer.
"""

from __future__ import annotations

from dgssi_platform.infrastructure.extraction.regex.extracteur_tableaux_chiffres import (
    extraire_resultats_par_element,
    extraire_taux_conformite_global,
)

# Extrait minimal et fidèle du vrai rapport — juste assez pour isoler le comportement,
# sans dépendre du fichier PDF ni de Docling dans ce test unitaire.
TABLEAU_TAUX_GLOBAL = [
    ["Taux de conformité à la DNSSI (Taux des règles mises en œuvre totalement)", "76,70%"]
]

TABLEAU_LEGENDE_CRITICITE = [
    ["CRITIQUE", "Il est impératif que des mesures soient prises immédiatement..."],
    ["ÉLEVÉE", "Il est impératif que des mesures soient prises dans un court délai..."],
    ["MOYENNE", "Des mesures doivent être prises dans un délai moyen..."],
    ["FAIBLE", "Il s'agit de notes d'information..."],
]

TABLEAU_RESULTATS_PAR_ELEMENT = [
    ["Architecture", "0", "0", "3", "2"],
    ["Firewall Central Forcepoint", "2", "0", "5", "1"],
    ["Firewall Partenaire", "3", "4", "9", "1"],
    ["Firewall Frontal", "3", "4", "9", "1"],
    ["Switch fédérateur", "2", "2", "7", "1"],
    ["Serveur de messagerie", "0", "16", "6", "2"],
    ["Serveur web Alpha", "6", "14", "7", "0"],
]


def test_taux_conformite_global_golden() -> None:
    tableaux = [TABLEAU_TAUX_GLOBAL]
    taux, confiance = extraire_taux_conformite_global(tableaux)

    assert taux == 76.7
    assert confiance == 1.0


def test_taux_conformite_absent_retourne_none() -> None:
    tableaux = [[["Un tableau sans rapport", "42"]]]
    taux, confiance = extraire_taux_conformite_global(tableaux)

    assert taux is None
    assert confiance < 0.5


def test_resultats_par_element_golden() -> None:
    tableaux = [TABLEAU_LEGENDE_CRITICITE, TABLEAU_RESULTATS_PAR_ELEMENT]
    resultats, confiance = extraire_resultats_par_element(tableaux)

    assert confiance == 1.0
    assert resultats["Serveur web Alpha"] == {
        "CRITIQUE": 6, "ELEVEE": 14, "MOYENNE": 7, "FAIBLE": 0,
    }
    assert resultats["Architecture"] == {
        "CRITIQUE": 0, "ELEVEE": 0, "MOYENNE": 3, "FAIBLE": 2,
    }
    assert len(resultats) == 7


def test_resultats_par_element_ne_confond_pas_legende_et_donnees() -> None:
    """Régression : la légende seule (2 colonnes) ne doit jamais être
    retournée comme résultat, même si elle contient les 4 mots-clés.
    """
    tableaux = [TABLEAU_LEGENDE_CRITICITE]  # légende seule, sans le vrai tableau
    resultats, confiance = extraire_resultats_par_element(tableaux)

    assert resultats == {}
    assert confiance < 0.5


def test_resultats_par_element_sans_voisin_a_confiance_reduite() -> None:
    """Sans légende adjacente, la confiance doit être plus basse que 1.0
    (bonus contextuel absent) — documente le comportement du score.
    """
    tableaux = [TABLEAU_RESULTATS_PAR_ELEMENT]  # pas de légende à proximité
    resultats, confiance = extraire_resultats_par_element(tableaux)

    assert len(resultats) == 7  # les données restent correctes
    assert confiance == 0.6  # score structurel seul (7 lignes × 0.1, plafonné à 0.6)
    assert confiance < 1.0  # mais inférieure au score avec bonus contextuel confirmé