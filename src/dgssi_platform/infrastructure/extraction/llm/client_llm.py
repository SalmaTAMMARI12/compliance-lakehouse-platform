"""Wrapper autour de llama-cpp-python (fichier .gguf local).
Remplace la version Ollama pour économiser la RAM (Ollama garde le modèle
en mémoire en permanence, llama-cpp-python le charge uniquement à la demande).
Contrat public identique — extracteur_constats.py inchangé.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from dgssi_platform.shared.logging import get_logger

import os

logger = get_logger(__name__)

_MODEL_PATH = Path(os.environ.get("LLM_MODEL_PATH", ""))
_llm_instance = None

_JSON_GRAMMAR = r'''
root   ::= object
object ::= "{" ws members? ws "}"
members ::= pair (ws "," ws pair)*
pair   ::= string ws ":" ws value
value  ::= object | array | string | number | ("true" | "false" | "null")
array  ::= "[" ws (value (ws "," ws value)*)? ws "]"
string ::= "\"" ([^"\\] | "\\" .)* "\""
number ::= "-"? [0-9]+ ("." [0-9]+)?
ws     ::= [ \t\n\r]*
'''

def _get_llm():
    global _llm_instance
    if _llm_instance is None:
        if not _MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Modèle LLM introuvable : {_MODEL_PATH}. "
                "Définis LLM_MODEL_PATH vers le fichier .gguf (voir README)."
            )
        from llama_cpp import Llama
        logger.info("Chargement du modèle LLM : %s", _MODEL_PATH)
        _llm_instance = Llama(
            model_path=str(_MODEL_PATH),
            n_ctx=4096,
            verbose=False
        )
    return _llm_instance


def generer_json_chat(
    system_prompt: str, user_prompt: str, max_tokens: int = 900
) -> tuple[dict[str, Any] | None, float]:
    """Appelle le LLM via create_chat_completion avec grammaire JSON forcée.
    Même contrat exact que la version Ollama — ne lève jamais d'exception,
    retourne (None, 0.0) en cas d'échec.
    """
    try:
        from llama_cpp import LlamaGrammar
        llm = _get_llm()
        grammar = LlamaGrammar.from_string(_JSON_GRAMMAR)
        reponse = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.1,
            repeat_penalty=1.1,
            grammar=grammar,
        )
        texte_brut = reponse["choices"][0]["message"]["content"]
        logger.debug("Texte brut LLM : %s", texte_brut[:2000])
        resultat = json.loads(texte_brut)
        return resultat, 0.7
    except Exception as e:
        logger.error("Échec de l'appel LLM ou du parsing JSON : %s", e)
        return None, 0.0
