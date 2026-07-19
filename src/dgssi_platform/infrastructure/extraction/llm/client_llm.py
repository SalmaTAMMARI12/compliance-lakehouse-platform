"""Wrapper autour de llama-cpp-python. Isolé dans ce fichier pour que le
reste du projet ne dépende jamais directement de llama_cpp.

Utilise create_chat_completion (pas l'appel de complétion brute) car
Qwen2.5-Instruct a été entraîné spécifiquement sur ce format ; l'appeler
en complétion brute produisait des sorties incohérentes (placeholders
recopiés, structures invalides) alors que l'API chat les élimine.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

_MODEL_PATH = Path("C:/Users/hp/Downloads/qwen2.5-1.5b-instruct-q4_k_m.gguf")
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
        from llama_cpp import Llama
        logger.info("Chargement du modèle LLM local : %s", _MODEL_PATH)
        _llm_instance = Llama(model_path=str(_MODEL_PATH), n_ctx=4096, verbose=False)
    return _llm_instance


def generer_json_chat(
    system_prompt: str, user_prompt: str, max_tokens: int = 600
) -> tuple[dict[str, Any] | None, float]:
    """Appelle le LLM via l'API chat (system + user), avec une grammaire
    JSON générique. Ne lève jamais d'exception vers l'appelant — retourne
    (None, 0.0) en cas d'échec, même contrat que les extracteurs regex.
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
        logger.debug("Texte brut LLM: %s", texte_brut[:2000])
        resultat = json.loads(texte_brut)
        return resultat, 0.7
    except Exception as e:
        logger.error("Échec de l'appel LLM ou du parsing JSON : %s", e)
        return None, 0.0
