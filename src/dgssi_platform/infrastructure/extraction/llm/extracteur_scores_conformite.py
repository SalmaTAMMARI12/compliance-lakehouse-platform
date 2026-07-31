"""Extraction LLM des résultats d'évaluation DNSSI — robuste face aux
variations de format entre prestataires d'audit.

Chaque prestataire PASSI utilise son propre système de notation :
pourcentage, note sur 5, lettre, répartition conforme/partiel/non-conforme,
graphe avec légende textuelle... Les regex ne peuvent pas absorber cette
variabilité. Le LLM (Qwen 2.5) comprend le contexte et normalise tout
en pourcentage 0-100 pour le pipeline data engineering.

Stratégie LLM-first :
1. Construit un texte enrichi (texte + tableaux formatés)
2. Extrait la section la plus pertinente (synthèse/résumé)
3. Appelle le LLM avec un prompt multi-notation
4. Valide le JSON retourné
5. Fallback regex si le LLM échoue

Le résultat peuple les champs Audit :
- taux_conformite_global (float, normalisé en %)
- systeme_notation_source (str, traçabilité)
- valeur_brute_source (str, traçabilité)
- prestataire_audit (str)
- repartition_globale_controles (dict)
- taux_par_chapitre (dict)
"""
from __future__ import annotations

from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_scores import (
    SYSTEM_PROMPT_SCORES,
    construire_user_prompt_scores,
)
from dgssi_platform.infrastructure.extraction.llm.texte_enrichi import (
    construire_texte_enrichi,
    extraire_section_synthese,
)
from dgssi_platform.infrastructure.extraction.regex.extracteur_tableaux_chiffres import (
    extraire_taux_conformite_global as extraire_taux_regex,
)
from dgssi_platform.infrastructure.extraction.regex.extracteur_texte_libre import (
    extraire_prestataire as extraire_prestataire_regex,
)
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def _valider_taux(valeur: object) -> float | None:
    """Valide et normalise un taux de conformité retourné par le LLM."""
    if valeur is None:
        return None
    try:
        taux = float(valeur)
    except (ValueError, TypeError):
        logger.warning("Taux de conformité invalide retourné par le LLM : %s", valeur)
        return None

    if taux < 0 or taux > 100:
        logger.warning("Taux de conformité hors bornes : %.2f", taux)
        return None

    return round(taux, 2)


def _valider_repartition(repartition: object) -> dict[str, float] | None:
    """Valide la répartition conforme/partiel/non_conforme."""
    if not isinstance(repartition, dict):
        return None

    cles_attendues = {"conforme", "partiel", "non_conforme"}
    resultat: dict[str, float] = {}

    for cle in cles_attendues:
        val = repartition.get(cle)
        if val is not None:
            try:
                resultat[cle] = round(float(val), 2)
            except (ValueError, TypeError):
                continue

    return resultat if resultat else None


def _valider_taux_par_chapitre(taux_dict: object) -> dict[str, float] | None:
    """Valide les taux par chapitre retournés par le LLM."""
    if not isinstance(taux_dict, dict):
        return None

    resultat: dict[str, float] = {}
    for chapitre, valeur in taux_dict.items():
        if not isinstance(chapitre, str) or not chapitre.strip():
            continue
        taux = _valider_taux(valeur)
        if taux is not None:
            resultat[chapitre.strip()] = taux

    return resultat if resultat else None


def extraire_scores_conformite(
    texte: str,
    tableaux: list[list[list[str]]],
) -> tuple[dict, float]:
    """Extrait les résultats d'évaluation DNSSI via LLM, avec fallback regex.

    Args:
        texte: Texte Markdown du rapport (Silver).
        tableaux: Tableaux extraits du rapport (Silver).

    Returns:
        Tuple (résultats, confiance). Résultats = dict avec les clés :
        - taux_conformite_global: float | None
        - systeme_notation: str
        - valeur_brute: str
        - repartition: dict | None
        - taux_par_chapitre: dict | None
        - prestataire: str | None
    """
    # Résultat par défaut
    resultat_vide = {
        "taux_conformite_global": None,
        "systeme_notation": "inconnu",
        "valeur_brute": "",
        "repartition": None,
        "taux_par_chapitre": None,
        "prestataire": None,
    }

    # Construire le texte enrichi et extraire la section synthèse
    texte_enrichi = construire_texte_enrichi(texte, tableaux)
    section = extraire_section_synthese(texte_enrichi, max_longueur=10000)

    if not section.strip():
        logger.warning("Section synthèse vide — impossible d'extraire les scores")
        return _fallback_regex(texte, tableaux, resultat_vide)

    # Appel LLM
    user_prompt = construire_user_prompt_scores(section)
    resultat_llm, confiance = generer_json_chat(
        SYSTEM_PROMPT_SCORES,
        user_prompt,
        max_tokens=600,
    )

    if resultat_llm is None:
        logger.warning("LLM n'a pas retourné de résultat — fallback regex")
        return _fallback_regex(texte, tableaux, resultat_vide)

    # Validation et normalisation
    taux = _valider_taux(resultat_llm.get("taux_conformite_global"))
    repartition = _valider_repartition(resultat_llm.get("repartition"))
    taux_par_chapitre = _valider_taux_par_chapitre(resultat_llm.get("taux_par_chapitre"))

    systeme = resultat_llm.get("systeme_notation", "inconnu")
    if not isinstance(systeme, str):
        systeme = "inconnu"

    valeur_brute = resultat_llm.get("valeur_brute", "")
    if not isinstance(valeur_brute, str):
        valeur_brute = str(valeur_brute) if valeur_brute is not None else ""

    prestataire = resultat_llm.get("prestataire")
    if isinstance(prestataire, str) and prestataire.strip():
        prestataire = prestataire.strip()
    else:
        prestataire = None

    resultat = {
        "taux_conformite_global": taux,
        "systeme_notation": systeme,
        "valeur_brute": valeur_brute,
        "repartition": repartition,
        "taux_par_chapitre": taux_par_chapitre,
        "prestataire": prestataire,
    }

    # Si le LLM n'a trouvé ni taux ni prestataire, tenter le fallback regex
    if taux is None and prestataire is None:
        logger.info("LLM n'a trouvé ni taux ni prestataire — fallback regex")
        return _fallback_regex(texte, tableaux, resultat)

    # Si le LLM a trouvé le taux mais pas le prestataire (ou l'inverse), compléter
    if taux is None:
        taux_regex, conf_regex = extraire_taux_regex(tableaux)
        if taux_regex is not None:
            resultat["taux_conformite_global"] = taux_regex
            resultat["systeme_notation"] = "pourcentage"
            resultat["valeur_brute"] = f"{taux_regex}%"
            logger.info("Taux complété par regex : %.2f%%", taux_regex)

    if prestataire is None:
        prestataire_regex, conf_prest = extraire_prestataire_regex(texte)
        if prestataire_regex:
            resultat["prestataire"] = prestataire_regex
            logger.info("Prestataire complété par regex : %s", prestataire_regex)

    logger.info(
        "Scores extraits par LLM — taux=%.2f%%, notation=%s, prestataire=%s (confiance=%.2f)",
        resultat["taux_conformite_global"] or 0.0,
        resultat["systeme_notation"],
        resultat["prestataire"] or "?",
        confiance,
    )
    return resultat, confiance


def _fallback_regex(
    texte: str,
    tableaux: list[list[list[str]]],
    resultat_base: dict,
) -> tuple[dict, float]:
    """Fallback complet sur les extracteurs regex existants."""
    resultat = dict(resultat_base)

    taux_regex, conf_taux = extraire_taux_regex(tableaux)
    if taux_regex is not None:
        resultat["taux_conformite_global"] = taux_regex
        resultat["systeme_notation"] = "pourcentage"
        resultat["valeur_brute"] = f"{taux_regex}%"

    prestataire_regex, conf_prest = extraire_prestataire_regex(texte)
    if prestataire_regex:
        resultat["prestataire"] = prestataire_regex

    confiance = max(conf_taux, conf_prest) * 0.8  # Pénalité car fallback
    logger.info(
        "Fallback regex — taux=%.2f%%, prestataire=%s (confiance=%.2f)",
        resultat.get("taux_conformite_global") or 0.0,
        resultat.get("prestataire") or "?",
        confiance,
    )
    return resultat, confiance
