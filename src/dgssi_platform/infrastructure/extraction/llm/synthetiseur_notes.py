"""Enrichissement LLM : Synthèse des notes d'audit.

Produit une synthèse neutre et factuelle des aspects positifs/existants
remontés par l'audit, sans jamais porter de jugement de conformité.
"""

from __future__ import annotations

from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT_NOTES = """Tu es un assistant technique neutre et objectif chargé de résumer des notes d'audit de sécurité.
Ton résumé doit comporter 3 à 5 phrases en français.
Contrat strict : 
- Décris fidèlement et de manière purement factuelle ce qui existe déjà (les points positifs ou actions en place).
- Ne formule JAMAIS de jugement de conformité. 
- Ne dis JAMAIS "ce chapitre est conforme", "les exigences sont respectées", ou "l'audité est en règle".
- Contente-toi de résumer les faits exposés dans le texte source.
Réponds TOUJOURS avec un objet JSON unique ayant une seule clé "notes_audit_synthese" contenant ton résumé sous forme de chaîne de caractères."""

def construire_user_prompt_notes(nom_chapitre: str, texte_notes: str) -> str:
    return f"""Chapitre : {nom_chapitre}

Texte brut des notes d'audit :
{texte_notes}

Résume ce texte en 3 à 5 phrases, de manière strictement factuelle et neutre, dans un objet JSON avec la clé "notes_audit_synthese"."""

def synthetiser_notes_chapitre(nom_chapitre: str, texte_notes: str) -> tuple[str | None, float]:
    """Appelle le LLM pour résumer les notes d'un chapitre.
    Retourne la synthèse et le score de confiance (0.0 en cas d'échec).
    """
    if not texte_notes.strip():
        return "", 1.0  # Si pas de notes, on retourne vide avec pleine confiance

    user_prompt = construire_user_prompt_notes(nom_chapitre, texte_notes)
    
    resultat, confiance = generer_json_chat(SYSTEM_PROMPT_NOTES, user_prompt, max_tokens=300)
    
    if resultat is None or not isinstance(resultat, dict):
        logger.warning("Échec de la synthèse LLM pour le chapitre %s", nom_chapitre)
        return None, 0.0
        
    synthese = resultat.get("notes_audit_synthese")
    if not isinstance(synthese, str) or not synthese.strip():
        logger.warning("Clé 'notes_audit_synthese' manquante ou invalide pour le chapitre %s", nom_chapitre)
        return None, 0.0
        
    return synthese.strip(), confiance
