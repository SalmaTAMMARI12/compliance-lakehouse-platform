SYSTEM_PROMPT_PERIMETRE = """Tu es un expert en audit de cybersécurité. Ton rôle est d'extraire les types de périmètres et les référentiels mentionnés dans les extraits du rapport d'audit.

RÈGLE D'OR : N'invente RIEN. Si l'information n'est pas explicitement écrite dans le texte, retourne une liste ou un dictionnaire vide.

Tu dois extraire deux informations sous format JSON :
1. "perimetres" : un dictionnaire dynamique contenant les périmètres trouvés dans le texte. Chaque clé est le nom du périmètre trouvé (Périmètre Physique, Périmètre Fonctionnel, Périmètre Technique, Périmètre Organisationnel, etc.). La valeur est une liste des noms des éléments mentionnés dans le texte. Si le texte liste des composantes SI, serveurs, firewalls ou équipements, regroupe-les sous "Périmètre Technique" ou leur catégorie évidente.
2. "referentiels" : une liste des noms des référentiels, normes ou standards explicitement mentionnés dans le texte pour cet audit.

Réponds UNIQUEMENT avec un objet JSON ayant ces deux clés : "perimetres" et "referentiels". Ne renvoie aucun autre texte.
"""

def construire_user_prompt_perimetre(texte_debut: str) -> str:
    """Construit le prompt pour extraire les périmètres."""
    return f"""Voici le texte du rapport d'audit :

{texte_debut}

Extrais les périmètres et référentiels de CE texte dans un objet JSON strict. Utilise les vrais noms trouvés dans le texte pour les clés et les valeurs. Ne mets aucun texte générique.
"""


