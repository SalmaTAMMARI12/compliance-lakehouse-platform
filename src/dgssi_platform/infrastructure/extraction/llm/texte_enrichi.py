"""Construction d'un texte enrichi fusionnant le texte Markdown et les tableaux
extraits d'un rapport d'audit DNSSI — destiné au LLM pour extraction sémantique.

Le problème : dans les rapports DOCX organisationnels, les constats, recommandations
et codes DNSSI se trouvent dans les tableaux, pas dans le texte Markdown. Le LLM
(extracteur_constats, extracteur_scores) ne travaillait que sur le texte et ne
voyait jamais ces données.

Cette fonction fusionne texte + tableaux en un seul bloc de texte lisible,
permettant au LLM de travailler sur la totalité du contenu du rapport.
"""
from __future__ import annotations

import re

from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

# Pattern pour détecter les codes DNSSI dans les cellules de tableau
_PATTERN_CODE_DNSSI = re.compile(
    r"^(?:DNSSI[-\s]*)?([A-Z]{2,8}(?:-[A-Z0-9/]+)+)\s*[:\-–]",
    re.IGNORECASE,
)

# Mots-clés structurels dans les cellules (début de cellule)
_MARQUEURS_STRUCTURELS = {
    "constat": "Constat",
    "recommandation": "Recommandation",
    "notes d'audit": "Notes d'audit",
    "preuves": "Preuves",
    "objectif": "Objectif",
    "points de contrôle": "Points de contrôle",
}


def _formater_tableau(tableau: list[list[str]], index: int) -> str:
    """Formate un tableau extrait en texte lisible pour le LLM.

    Stratégie :
    - Si une cellule commence par un code DNSSI → titre de section
    - Si une cellule commence par un marqueur structurel → sous-titre
    - Sinon → contenu brut
    - Les cellules vides sont ignorées
    """
    lignes_formatees: list[str] = []
    code_courant: str | None = None

    for ligne in tableau:
        for cellule in ligne:
            texte = str(cellule).strip()
            if not texte:
                continue

            # Détection d'un code DNSSI → titre de section
            m = _PATTERN_CODE_DNSSI.match(texte)
            if m:
                code_courant = m.group(1).upper()
                # Prend tout le texte de la cellule comme titre (code + libellé)
                lignes_formatees.append(f"\n--- [{texte.strip()}] ---")
                continue

            # Détection d'un marqueur structurel
            texte_lower = texte.lower()
            marqueur_trouve = False
            for cle, label in _MARQUEURS_STRUCTURELS.items():
                if texte_lower.startswith(cle):
                    # Séparer le marqueur du contenu
                    contenu = re.sub(
                        rf"^{re.escape(cle)}\s*:?\s*",
                        "",
                        texte,
                        flags=re.IGNORECASE,
                    ).strip()
                    if contenu:
                        lignes_formatees.append(f"{label} : {contenu}")
                    else:
                        lignes_formatees.append(f"{label} :")
                    marqueur_trouve = True
                    break

            if not marqueur_trouve:
                # Contenu brut — on le garde s'il est substantiel
                if len(texte) > 3:
                    lignes_formatees.append(texte)

    if not lignes_formatees:
        return ""

    return "\n".join(lignes_formatees)


def construire_texte_enrichi(
    texte_markdown: str,
    tableaux: list[list[list[str]]],
    max_longueur: int | None = None,
) -> str:
    """Fusionne le texte Markdown et les tableaux en un seul bloc de texte
    lisible par le LLM.

    Le texte enrichi a la structure :
    1. Le texte Markdown original (souvent vide/pauvre pour les DOCX)
    2. Une section "=== CONTENU DES TABLEAUX ===" avec chaque tableau formaté

    Args:
        texte_markdown: Le texte Markdown extrait du document (Silver).
        tableaux: Les tableaux extraits (Silver), format list[list[list[str]]].
        max_longueur: Si spécifié, tronque le résultat à ce nombre de caractères.
            Le LLM a un contexte limité (4096 tokens ≈ ~12000 caractères FR).
            None = pas de troncature.

    Returns:
        Le texte enrichi complet, prêt à être envoyé au LLM.
    """
    parties: list[str] = []

    # Partie 1 : texte Markdown (peut être vide pour les rapports DOCX)
    if texte_markdown.strip():
        parties.append(texte_markdown.strip())

    # Partie 2 : tableaux formatés en texte lisible
    tableaux_formetes: list[str] = []
    for i, tableau in enumerate(tableaux):
        texte_tableau = _formater_tableau(tableau, i)
        if texte_tableau:
            tableaux_formetes.append(texte_tableau)

    if tableaux_formetes:
        parties.append("\n=== CONTENU DES TABLEAUX ===\n")
        parties.append("\n\n".join(tableaux_formetes))

    resultat = "\n\n".join(parties)

    if max_longueur and len(resultat) > max_longueur:
        logger.info(
            "Texte enrichi tronqué : %d → %d caractères",
            len(resultat),
            max_longueur,
        )
        resultat = resultat[:max_longueur]

    logger.info(
        "Texte enrichi construit : %d caractères (texte=%d, %d tableaux formatés)",
        len(resultat),
        len(texte_markdown),
        len(tableaux_formetes),
    )
    return resultat


def extraire_section_synthese(
    texte_enrichi: str,
    max_longueur: int = 10000,
) -> str:
    """Extrait la partie la plus pertinente pour les scores d'évaluation.

    Les sections de synthèse/résumé (généralement en début de rapport) contiennent
    presque toujours les taux de conformité et scores globaux. Cette fonction
    réduit le texte au strict nécessaire pour l'extraction des scores, en restant
    dans le budget de contexte du LLM.

    Recherche par ordre de priorité :
    1. Section contenant "taux de conformité" ou "niveau de maturité" ou "score"
    2. Section "synthèse" ou "résumé" ou "résultats"
    3. Les premiers max_longueur caractères si rien trouvé
    """
    texte_lower = texte_enrichi.lower()

    # Mots-clés prioritaires pour trouver la section des scores
    mots_cles_scores = [
        "taux de conformité",
        "niveau de maturité",
        "score global",
        "résultat global",
        "conformité globale",
        "évaluation globale",
        "synthèse des résultats",
        "résultats de l'audit",
        "bilan de conformité",
    ]

    # Chercher une fenêtre de texte autour de chaque mot-clé
    meilleures_positions: list[int] = []
    for mot in mots_cles_scores:
        idx = texte_lower.find(mot)
        if idx != -1:
            meilleures_positions.append(idx)

    if meilleures_positions:
        # Prendre la position la plus précoce et extraire une fenêtre large
        debut = max(0, min(meilleures_positions) - 500)
        fin = min(len(texte_enrichi), debut + max_longueur)
        extrait = texte_enrichi[debut:fin]
        logger.info(
            "Section synthèse trouvée (position %d-%d, %d chars)",
            debut, fin, len(extrait),
        )
        return extrait

    # Fallback : début du texte (les synthèses sont presque toujours au début)
    logger.info(
        "Section synthèse non trouvée par mots-clés, utilisation du début (%d chars)",
        min(max_longueur, len(texte_enrichi)),
    )
    return texte_enrichi[:max_longueur]
