"""Extracteur regex pour les tableaux chiffrés du rapport PASSI.

Détection combinant mots-clés ET structure — l'un sans l'autre produit des
faux positifs (vérifié empiriquement : une légende à 2 colonnes contenant
les 4 niveaux de criticité battait le vrai tableau de données avant cette
correction).
"""

from __future__ import annotations

from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

_CRITICITES = {"CRITIQUE", "ELEVEE", "ÉLEVÉE", "MOYENNE", "FAIBLE"}
_SEUIL_CONFIANCE_MINIMAL = 0.5


def extraire_taux_conformite_global(
    tableaux: list[list[list[str]]],
) -> tuple[float | None, float]:
    """Cherche une LIGNE contenant à la fois 'Taux de conformité' et un %."""
    meilleur_score = 0.0
    meilleure_valeur: float | None = None

    for tableau in tableaux:
        for ligne in tableau:
            texte_ligne = " ".join(ligne)
            if "Taux de conformité" not in texte_ligne:
                continue

            score = 0.5
            if "DNSSI" in texte_ligne:
                score += 0.3

            for cellule in ligne:
                if "%" in cellule:
                    brut = cellule.replace("%", "").replace(",", ".").strip()
                    try:
                        valeur = float(brut)
                        score = min(1.0, score + 0.2)
                        if score > meilleur_score:
                            meilleur_score = score
                            meilleure_valeur = valeur
                    except ValueError:
                        continue

    if meilleur_score < _SEUIL_CONFIANCE_MINIMAL:
        logger.warning("Taux de conformité global : confiance insuffisante (%.2f)", meilleur_score)
        return None, meilleur_score

    return meilleure_valeur, meilleur_score


def extraire_resultats_par_element(
    tableaux: list[list[list[str]]],
) -> tuple[dict[str, dict[str, int]], float]:
    """Un tableau n'est candidat QUE s'il a au moins une ligne à 5 colonnes
    avec 4 valeurs numériques — la structure prime sur les mots-clés seuls.

    Le score est ensuite enrichi si un tableau VOISIN (index -1 ou +1)
    contient les mots-clés de criticité — hypothèse que Docling préserve
    l'ordre de lecture, donc une légende reste proche de son tableau de
    données. Heuristique locale, pas une garantie.
    """
    meilleur_score = 0.0
    meilleur_index = -1
    meilleurs_resultats: dict[str, dict[str, int]] = {}

    for i, tableau in enumerate(tableaux):
        resultats: dict[str, dict[str, int]] = {}
        lignes_valides = 0

        for ligne in tableau:
            if len(ligne) != 5:
                continue
            nom_element, critique, elevee, moyenne, faible = ligne
            try:
                resultats[nom_element] = {
                    "CRITIQUE": int(critique),
                    "ELEVEE": int(elevee),
                    "MOYENNE": int(moyenne),
                    "FAIBLE": int(faible),
                }
                lignes_valides += 1
            except ValueError:
                continue

        if lignes_valides == 0:
            continue

        score_structure = min(0.6, 0.1 * lignes_valides)

        cellules_locales = {c.strip().upper() for ligne in tableau for c in ligne}
        voisins_indices = [j for j in (i - 1, i + 1) if 0 <= j < len(tableaux)]
        cellules_voisines = {
            c.strip().upper()
            for j in voisins_indices
            for ligne in tableaux[j]
            for c in ligne
        }
        nb_criticites_contexte = len((cellules_locales | cellules_voisines) & _CRITICITES)
        bonus_contexte = (nb_criticites_contexte / 4) * 0.4

        score = min(1.0, score_structure + bonus_contexte)

        if score > meilleur_score:
            meilleur_score = score
            meilleur_index = i
            meilleurs_resultats = resultats

    if meilleur_score < _SEUIL_CONFIANCE_MINIMAL:
        logger.warning("Résultats par élément : confiance insuffisante (%.2f)", meilleur_score)
        return {}, meilleur_score

    logger.info(
        "Résultats par élément trouvés au tableau %d, confiance %.2f",
        meilleur_index,
        meilleur_score,
    )
    return meilleurs_resultats, meilleur_score