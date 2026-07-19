from pathlib import Path
from llama_cpp import Llama, LlamaGrammar
import json

from dgssi_platform.infrastructure.extraction.regex.decoupage_chapitres import trouver_ancres_chapitres

JSON_GRAMMAR = r'''
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

texte = Path("texte_complet_rapport.md").read_text(encoding="utf-8")
ancres = trouver_ancres_chapitres(texte)

# Chapitre 10 = "Acquisition, développement et maintenance..." (index 9)
i = 9
debut = ancres[i].start()
fin = ancres[i + 1].start() if i + 1 < len(ancres) else len(texte)
bloc_complet = texte[debut:fin]

print("=== Bloc envoyé au LLM (longueur:", len(bloc_complet), ") ===")
print(bloc_complet)
print()

llm = Llama(model_path="C:/Users/hp/Downloads/qwen2.5-1.5b-instruct-q4_k_m.gguf", n_ctx=4096, verbose=False)
grammar = LlamaGrammar.from_string(JSON_GRAMMAR)

SYSTEM_PROMPT = """Tu es un assistant qui analyse un extrait désordonné d'un rapport d'audit DNSSI (norme marocaine de cybersécurité).
Le texte contient plusieurs sections mélangées : Clauses, Objectifs, Points de contrôle, Notes d'audit, Preuves, et Constats.
Ta tâche est d'identifier UNIQUEMENT le texte qui correspond à la section "Constats" (les écarts/problèmes réellement relevés par l'auditeur), en ignorant tout le reste.
DNSSI est le nom du référentiel réglementaire évalué, pas un système informatique.
Réponds avec un objet JSON ayant une clé ecarts contenant un tableau d'objets {description, recommandation}."""

user_prompt = f"""Voici l'extrait complet et désordonné du chapitre :

{bloc_complet}

Identifie uniquement les VRAIS constats (écarts constatés par l'auditeur) dans ce texte — pas les objectifs, pas les points de contrôle, pas les notes d'audit positives, pas les preuves listées.
S'il n'y a aucun constat clair, réponds avec un tableau vide.
Pour chaque constat trouvé, donne une description qui REFORMULE le constat en français (max 30 mots) et une recommandation si explicitement mentionnée, sinon null."""

reponse = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ],
    max_tokens=600,
    temperature=0.1,
    repeat_penalty=1.1,
    grammar=grammar,
)
texte_sortie = reponse["choices"][0]["message"]["content"]
print("=== Résultat LLM ===")
try:
    parsed = json.loads(texte_sortie)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
except Exception as e:
    print("Erreur JSON:", e, "| Brut:", texte_sortie)
