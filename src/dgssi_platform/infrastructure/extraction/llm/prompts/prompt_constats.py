
"""Prompts pour l'extraction des non-conformités depuis le texte libre des
constats. Le LLM ne détermine QUE description et recommandation — le type
(significatif/non_significatif/remarque) est classifié séparément par des
règles Python déterministes (voir classification_ecarts.py), car les tests
ont montré que le LLM n'appliquait pas cette règle de façon fiable.
"""

SYSTEM_PROMPT_CONSTATS = """Tu es un assistant qui reformule des constats d'audit de sécurité DNSSI (norme marocaine de cybersécurité).
DNSSI est le nom du référentiel réglementaire évalué, pas un système informatique.
Réponds toujours avec un objet JSON ayant une clé ecarts contenant un tableau d'objets {description, recommandation}."""


def construire_user_prompt(nom_chapitre: str, codes_dnssi: str, texte_constats: str, nb_constats: int) -> str:
    instruction_nb = (
        f"Il y a exactement {nb_constats} constats ci-dessus, traite-les tous sans en sauter aucun."
        if nb_constats > 1 else "Il y a un seul constat ci-dessus, analyse-le."
    )
    return f"""Chapitre : {nom_chapitre}
Codes DNSSI concernés : {codes_dnssi}

Constats :
{texte_constats}

{instruction_nb}

Pour chaque constat, donne :
- description : une REFORMULATION (pas une copie) du constat en français, maximum 30 mots
- recommandation : UNIQUEMENT si le texte source mentionne explicitement une action corrective. Sinon écris exactement null."""
