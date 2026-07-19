"""Extraction des écarts (constats + recommandations) par LLM local,
combinée à la détection de zones par regex (même logique par ordre
d'apparition que extracteur_clauses.py — réutilisée ici pour délimiter le
texte libre associé à chaque chapitre, pas seulement les codes).

Le LLM ne fait QUE le travail de compréhension de texte libre. Toute la
structure (quel texte appartient à quel chapitre) reste déterministe,
donc généralisable à n'importe quel rapport tant que le format
"DNSSI (codes)" ... texte libre ... "DNSSI (codes suivants)" est respecté.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from llama_cpp import Llama

_PATTERN_CLAUSES = re.compile(r"DNSSI\s*\(([^)]+)\)")

PROMPT_TEMPLATE = """Tu es un assistant qui extrait des données structurées à partir de rapports d'audit de sécurité DNSSI (norme marocaine de cybersécurité).

Voici la section "Constats" d'un chapitre du rapport, ainsi que son contexte :

Chapitre : {nom_chapitre}
Codes DNSSI concernés : {codes_dnssi}

Constats :
{texte_constats}

Pour chaque constat listé, extrait les informations suivantes :
- type : classe le constat parmi "significatif", "non_significatif", ou "remarque". Si le type n'est pas explicite, déduis-le du niveau de risque décrit (absence totale d'un contrôle = significatif ; processus en cours de finalisation ou de validation = non_significatif ; amélioration mineure sans risque = remarque).
- description : reformule le constat en une phrase claire et concise (max 30 mots), sans rien inventer.
- recommandation : si une action corrective est explicitement ou implicitement suggérée dans le texte, résume-la en une phrase. Sinon, écris null.

Règles strictes :
- N'invente aucune information absente du texte fourni.
- Traite TOUS les constats listés, sans en oublier aucun.
- Si le chapitre ne contient aucun écart (ex. "Conforme aux exigences. Aucun écart relevé."), réponds avec un tableau vide.

Format de sortie strict, JSON uniquement, sans texte avant ou après :
{{"ecarts": [{{"type": "...", "description": "...", "recommandation": "..." ou null}}]}}"""


@dataclass
class ZoneChapitre:
    nom_chapitre: str
    codes: list[str]
    texte_constats: str


def extraire_zones_par_chapitre(
    texte: str, noms_chapitres_ordonnes: list[str]
) -> list[ZoneChapitre]:
    """Découpe le texte en zones par chapitre, dans l'ordre d'apparition —
    même principe que extraire_clauses_par_chapitre : le texte ENTRE deux
    occurrences consécutives de "DNSSI (...)" appartient au chapitre
    correspondant au premier des deux blocs."""
    matches = list(_PATTERN_CLAUSES.finditer(texte))
    zones = []
    for i, match in enumerate(matches):
        if i >= len(noms_chapitres_ordonnes):
            break
        codes = [c.strip().rstrip(".").strip() for c in match.group(1).split(",")]
        debut = match.end()
        fin = matches[i + 1].start() if i + 1 < len(matches) else len(texte)
        texte_zone = texte[debut:fin].strip()
        zones.append(ZoneChapitre(
            nom_chapitre=noms_chapitres_ordonnes[i],
            codes=codes,
            texte_constats=texte_zone,
        ))
    return zones


def generer_ecarts(llm: Llama, zone: ZoneChapitre) -> list[dict]:
    """Appelle le LLM sur une zone, marque a_verifier=True pour tout écart
    significatif ou non_significatif — supervision humaine obligatoire
    avant intégration en base, le modèle s'étant déjà trompé sur ce type
    de classification lors des tests."""
    if not zone.texte_constats or "aucun écart" in zone.texte_constats.lower():
        return []

    prompt = PROMPT_TEMPLATE.format(
        nom_chapitre=zone.nom_chapitre,
        codes_dnssi=", ".join(zone.codes),
        texte_constats=zone.texte_constats,
    )
    reponse = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    contenu = reponse["choices"][0]["message"]["content"]

    try:
        donnees = json.loads(contenu)
    except json.JSONDecodeError:
        return [{"type": "erreur_parsing", "description": contenu[:200], "recommandation": None, "a_verifier": True}]

    ecarts = donnees.get("ecarts", [])
    for ecart in ecarts:
        ecart["a_verifier"] = ecart.get("type") in ("significatif", "non_significatif")
    return ecarts


def extraire_ecarts_tous_chapitres(
    texte: str, noms_chapitres_ordonnes: list[str], model_path: str
) -> dict[str, list[dict]]:
    """Point d'entrée principal : traite un rapport complet, chapitre par
    chapitre. Réutilisable sur n'importe quel rapport tant que le format
    DNSSI (...) est respecté dans le Silver."""
    llm = Llama(model_path=model_path, n_ctx=4096, verbose=False)
    zones = extraire_zones_par_chapitre(texte, noms_chapitres_ordonnes)

    resultats = {}
    for zone in zones:
        print(f"Traitement LLM: {zone.nom_chapitre}...")
        resultats[zone.nom_chapitre] = generer_ecarts(llm, zone)
    return resultats