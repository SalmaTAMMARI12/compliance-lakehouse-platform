"""Extraction du périmètre via LLM."""

import json
import logging
from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_perimetre import (
    SYSTEM_PROMPT_PERIMETRE,
    construire_user_prompt_perimetre,
)

logger = logging.getLogger(__name__)

def extraire_perimetre_llm(texte: str) -> tuple[dict[str, list[str]], list[str], float]:
    lignes = texte.split('\n')
    mots_cles = ['périmètre', 'perimetre', 'primtre', 'architecture', 'englobe les composantes']
    lignes_pertinentes = [i for i, l in enumerate(lignes) if any(m in l.lower() for m in mots_cles) and '...' not in l and '|' not in l]
    
    context_blocks = []
    for i in lignes_pertinentes:
        start = max(0, i - 2)
        end = min(len(lignes), i + 10)
        context_blocks.append('\\n'.join(lignes[start:end]))
    
    texte_context = '\\n\\n--- PARAGRAPH ---\\n\\n'.join(context_blocks)
    if not texte_context.strip():
        texte_context = texte[:8000]
    else:
        texte_context = texte_context[:10000] # Strict limit to avoid exceeding context window (10k chars = ~2.5k tokens)
        
    prompt = construire_user_prompt_perimetre(texte_context)
    
    try:
        data, conf = generer_json_chat(SYSTEM_PROMPT_PERIMETRE, prompt)
        
        perimetres = {}
        referentiels = []
        if data and isinstance(data, dict):
            raw_perimetres = data.get("perimetres", {})
            if isinstance(raw_perimetres, dict):
                for k, v in raw_perimetres.items():
                    if isinstance(v, list):
                        perimetres[k] = [str(x) for x in v]
                    else:
                        perimetres[k] = [str(v)]
                        
            raw_refs = data.get("referentiels", [])
            if isinstance(raw_refs, list):
                referentiels = [str(x) for x in raw_refs]
                
        return perimetres, referentiels, conf
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des périmètres via LLM: {e}")
        return {}, [], 0.0
