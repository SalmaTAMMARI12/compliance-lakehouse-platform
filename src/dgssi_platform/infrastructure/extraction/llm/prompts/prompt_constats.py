"""Prompts pour l'enrichissement documentaire des constats. Le LLM ne
produit QUE des champs d'extraction (résumé, recommandation si explicite,
actifs concernés, échéance si mentionnée) — jamais de classification ou
de décision de conformité, qui restent hors de son périmètre.
"""

SYSTEM_PROMPT_CONSTATS = """Tu es un assistant qui enrichit des constats d'audit de sécurité DNSSI (norme marocaine de cybersécurité).
DNSSI est le nom du référentiel réglementaire évalué, pas un système informatique.
Tu ne dois JAMAIS juger si un constat est conforme, significatif, critique ou non — cette décision n'est pas de ton ressort.
Réponds toujours avec un objet JSON ayant une clé ecarts contenant un tableau d'objets {resume_constat, recommandation, actifs_concernes, echeance}."""


def construire_user_prompt(nom_chapitre: str, texte_constats: str, nb_constats: int) -> str:
    instruction_nb = (
        f"Il y a exactement {nb_constats} constats ci-dessus, traite-les tous sans en sauter aucun."
        if nb_constats > 1 else "Il y a un seul constat ci-dessus, analyse-le."
    )
    return f"""Chapitre : {nom_chapitre}

Constats :
{texte_constats}

{instruction_nb}

Pour chaque constat, donne :
- resume_constat : une REFORMULATION (pas une copie) du constat en français, maximum 30 mots
- recommandation : UNIQUEMENT si le texte source mentionne explicitement une action corrective. Sinon null.
- actifs_concernes : liste des systèmes/équipements/serveurs explicitement nommés dans ce constat. Liste vide si aucun.
- echeance : UNIQUEMENT si une date ou période est explicitement mentionnée dans ce constat (ex. "T1-2024"). Sinon null.

N'invente jamais une information absente du texte source."""
