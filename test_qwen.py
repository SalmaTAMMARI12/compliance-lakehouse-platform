from llama_cpp import Llama, LlamaGrammar
import json

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

VALEURS_RECOMMANDATION_INVALIDES = {"N/A", "NA", "", "AUCUNE", "AUCUN"}


def classifier_type_ecart(texte_constat: str) -> str:
    texte = texte_constat.lower()
    marqueurs_absence = ["absence de", "absence d'", "aucun", "aucune", "n'est pas", "ne dispose pas", "non conforme"]
    marqueurs_en_cours = ["en cours de validation", "en cours d'instauration", "en cours de finalisation", "en cours de réalisation"]
    marqueurs_planifie = ["planifié", "prévu pour", "sera", "procèdera", "à l'issue de"]
    if any(m in texte for m in marqueurs_absence):
        return "significatif"
    if any(m in texte for m in marqueurs_en_cours):
        return "non_significatif"
    if any(m in texte for m in marqueurs_planifie):
        return "remarque"
    return "non_significatif"


def valider_extraction(item: dict) -> tuple[bool, str]:
    if not isinstance(item, dict):
        return False, "n'est pas un objet"
    description = item.get("description", "")
    if not isinstance(description, str) or len(description.strip()) < 5:
        return False, "description vide ou trop courte"
    recommandation = item.get("recommandation")
    if recommandation is not None and str(recommandation).strip().upper() in VALEURS_RECOMMANDATION_INVALIDES:
        return False, f"recommandation invalide: {recommandation!r}"
    return True, "ok"


llm = Llama(model_path="C:/Users/hp/Downloads/qwen2.5-1.5b-instruct-q4_k_m.gguf", n_ctx=4096, verbose=False)
grammar = LlamaGrammar.from_string(JSON_GRAMMAR)

cas_test = [
    {
        "nom_chapitre": "Gestion des actifs informationnels",
        "codes_dnssi": "ACTIF-RESP-INV, ACTIF-RESP-PROP, ACTIF-RESP-CHARTE, ACTIF-CLASSIF-INFO",
        "texte_constats": """- Absence d'un inventaire complet, consolidé et mis à jour de l'ensemble des actifs (matériels et logiciels) avec leurs versions, les correctifs appliqués, les n° de License etc.
- La dernière version de la charte est en cours de validation par la hiérarchie et le processus de sa communication et signature par l'ensemble des collaborateurs et personnes concernées est en cours d'instauration ;
- A l'issue de l'exercice de classification planifié pour 2024, l'audité procèdera à la déclaration actualisée des SI Sensibles conformément à la loi 05-20.""",
    },
    {
        "nom_chapitre": "Cryptographie",
        "codes_dnssi": "CRYPTO-MES-POL, CRYPTO-MES-GESTCLE",
        "texte_constats": "- La politique de gestion des clés cryptographiques a été élaborée et est en cours de validation.",
    },
]

SYSTEM_PROMPT = """Tu es un assistant qui reformule des constats d'audit de sécurité DNSSI (norme marocaine de cybersécurité).
DNSSI est le nom du référentiel réglementaire évalué, pas un système informatique.
Réponds toujours avec un objet JSON ayant une clé ecarts contenant un tableau d'objets {description, recommandation}."""

for cas in cas_test:
    lignes_constats = [l for l in cas["texte_constats"].split("\n") if l.strip().startswith("-")]
    nb_constats = len(lignes_constats)
    instruction_nb = (
        f"Il y a exactement {nb_constats} constats ci-dessus, traite-les tous sans en sauter aucun."
        if nb_constats > 1 else "Il y a un seul constat ci-dessus, analyse-le."
    )

    user_prompt = f"""Chapitre : {cas['nom_chapitre']}
Codes DNSSI concernés : {cas['codes_dnssi']}

Constats :
{cas['texte_constats']}

{instruction_nb}

Pour chaque constat, donne :
- description : une REFORMULATION (pas une copie) du constat en français, maximum 30 mots
- recommandation : UNIQUEMENT si le texte source mentionne explicitement une action corrective. Sinon écris exactement null."""

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
    texte = reponse["choices"][0]["message"]["content"]
    print(f"=== {cas['nom_chapitre']} ===")
    try:
        parsed = json.loads(texte)
        items_bruts = parsed.get("ecarts", [])
        resultats = []
        for i, item in enumerate(items_bruts):
            ok, raison = valider_extraction(item)
            if not ok:
                print(f"  [rejeté] {raison} -> {item}")
                continue
            texte_source = lignes_constats[i] if i < len(lignes_constats) else ""
            resultats.append({
                "type": classifier_type_ecart(texte_source),
                "description": item["description"],
                "recommandation": item.get("recommandation"),
            })
        print(json.dumps(resultats, indent=2, ensure_ascii=False))
        print(f"-> {len(resultats)}/{len(items_bruts)} valides (attendu: {nb_constats})")
    except Exception as e:
        print("Erreur JSON:", e, "| Brut:", texte)
    print()
