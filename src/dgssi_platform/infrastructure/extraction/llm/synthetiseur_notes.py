"""Enrichissement LLM : Synthèse des notes d'audit.

Produit une synthèse neutre et factuelle des aspects positifs/existants
ou des constats remontés par l'audit, sans jamais porter de jugement de conformité.
"""

from __future__ import annotations

from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_synthese import (
    SYSTEM_PROMPT_SYNTHESE,
    construire_user_prompt_synthese,
)
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def synthetiser_notes_chapitre(
    nom_chapitre: str, 
    texte_source: str, 
    est_constats: bool = False
) -> tuple[str | None, float]:
    """Appelle le LLM pour résumer les notes ou constats d'un chapitre.
    Retourne la synthèse et le score de confiance (0.0 en cas d'échec).
    """
    if not texte_source.strip():
        return "", 1.0  # Si pas de texte, on retourne vide avec pleine confiance

    user_prompt = construire_user_prompt_synthese(
        nom_chapitre, 
        texte_source, 
        est_constats=est_constats
    )
    
    resultat, confiance = generer_json_chat(
        SYSTEM_PROMPT_SYNTHESE, 
        user_prompt, 
        max_tokens=300
    )
    
    if resultat is None or not isinstance(resultat, dict):
        logger.warning("Échec de la synthèse LLM pour le chapitre %s", nom_chapitre)
        return None, 0.0
        
    synthese = resultat.get("notes_audit_synthese")
    if not isinstance(synthese, str) or not synthese.strip():
        logger.warning("Clé 'notes_audit_synthese' manquante ou invalide pour le chapitre %s", nom_chapitre)
        return None, 0.0
        
    return synthese.strip(), confiance
