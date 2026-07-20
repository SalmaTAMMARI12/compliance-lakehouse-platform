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

i = 13  # "Conformité", dernier chapitre
debut = ancres[i].start()
fin = len(texte)
bloc = texte[debut:fin]

idx = bloc.find("Constats")
section = bloc[idx + len("Constats"):].strip(" :\n")[:1500]
lignes = [l.strip() for l in section.split("\n") if l.strip().startswith("-")]

print("=== Constats bruts du chapitre Conformité ===")
for l in lignes:
    print(repr(l))
print()

from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_constats import SYSTEM_PROMPT_CONSTATS, construire_user_prompt

prompt = construire_user_prompt("Conformité", "\n".join(lignes), len(lignes))

llm = Llama(model_path="C:/Users/hp/Downloads/qwen2.5-1.5b-instruct-q4_k_m.gguf", n_ctx=4096, verbose=False)
grammar = LlamaGrammar.from_string(JSON_GRAMMAR)

reponse = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT_CONSTATS},
        {"role": "user", "content": prompt},
    ],
    max_tokens=900,
    temperature=0.1,
    repeat_penalty=1.1,
    grammar=grammar,
)
texte_brut = reponse["choices"][0]["message"]["content"]
print("=== Sortie BRUTE du LLM (avant parsing JSON) ===")
print(repr(texte_brut))
