"""Prompts pour la synthèse LLM par chapitre.

Deux cas d'usage pris en charge :
1. Synthèse depuis une section "Notes d'audit" explicite.
2. Synthèse depuis une liste de constats/écarts (quand la section notes est absente).
"""

SYSTEM_PROMPT_SYNTHESE = """Tu es un auditeur expert en cybersécurité (norme DNSSI).
Ton rôle est de rédiger une courte synthèse (3 à 5 phrases) de l'état d'un chapitre, à destination d'un comité de direction.

RÈGLES STRICTES :
1. Sois purement factuel et objectif.
2. Résume les points clés (forces ou faiblesses) mentionnés dans le texte fourni.
3. Ne porte AUCUN jugement de conformité global (ne dis jamais "ce chapitre est conforme" ou "l'entité respecte les exigences").
4. Ne fais pas de copier-coller, synthétise intelligemment le propos.

Réponds TOUJOURS avec un objet JSON unique ayant une seule clé "notes_audit_synthese" contenant ton résumé sous forme de chaîne de caractères."""


def construire_user_prompt_synthese(nom_chapitre: str, texte_source: str, est_constats: bool = False) -> str:
    """Construit le prompt utilisateur pour la synthèse.
    
    Args:
        nom_chapitre: Le nom du chapitre audité.
        texte_source: Le texte à synthétiser (notes ou liste de constats).
        est_constats: True si le texte est une liste de constats au lieu d'un paragraphe de notes.
    """
    source_type = "Liste des constats/écarts relevés" if est_constats else "Notes d'observations générales"
    
    return f"""Chapitre audité : {nom_chapitre}

{source_type} :
{texte_source}

Rédige une synthèse managériale de ces éléments en 3 à 5 phrases (factuelle, neutre, sans jugement de conformité global).
Retourne un JSON avec la clé "notes_audit_synthese"."""
