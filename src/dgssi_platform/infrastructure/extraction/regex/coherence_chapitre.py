"""Vérification de cohérence thématique entre un chapitre attendu et le
texte extrait pour ce chapitre. Nécessaire car Docling associe parfois mal
le texte au bon chapitre sur les tableaux multi-pages (voir investigation
du 19/07 : ~50% des chapitres concernés sur le rapport de référence).

Principe volontairement simple : les codes DNSSI du chapitre contiennent
déjà des racines de mots thématiques (ex. CRYPTO-MES-POL -> "crypto").
Si aucune de ces racines n'apparaît dans la description générée, c'est un
signal fort que le texte extrait appartient à un autre chapitre.
"""

from __future__ import annotations

import re


def _extraire_racines_thematiques(codes_dnssi: list[str]) -> set[str]:
    """Extrait des racines de mots à partir des codes DNSSI d'un chapitre.
    Ex. ['CRYPTO-MES-POL', 'CRYPTO-MES-GESTCLE'] -> {'crypto', 'mes', 'gestcle'}
    On ne garde que les segments de 4+ lettres pour éviter le bruit
    (ex. 'POL', 'RH' seuls ne sont pas assez spécifiques).
    """
    racines = set()
    for code in codes_dnssi:
        segments = re.split(r"[-/]", code.lower())
        for seg in segments:
            seg = seg.strip()
            if len(seg) >= 4 and seg.isalpha():
                racines.add(seg)
    return racines


_MARQUEURS_NEGATIFS = [
    "n'est pas", "ne sont pas", "ne dispose pas", "absence de", "aucun",
    "aucune", "non conforme", "ne couvre pas", "en cours de", "pas encore",
    "pas validé", "non validé", "incomplet", "défaut de", "manque de"
]

def est_coherent_avec_chapitre(description: str, codes_dnssi: list[str], texte_source: str = "") -> bool:
    """Retourne True si la description semble appartenir au bon chapitre,
    False si aucun signal thématique ne correspond (à vérifier manuellement).
    Vérifie également la présence de formulations négatives typiques d'un écart."""
    racines = _extraire_racines_thematiques(codes_dnssi)
    
    texte_complet = (description + " " + texte_source).lower()
    
    # 1. Vérification thématique
    est_thematique = True
    if racines:
        est_thematique = any(racine in texte_complet for racine in racines)
        
    # 2. Vérification de la formulation (si on a la source originale)
    est_negatif = True
    if texte_source:
        est_negatif = any(m in texte_complet for m in _MARQUEURS_NEGATIFS)
        
    # Si le texte source a été fourni, on exige au moins l'un des deux signaux
    if texte_source:
        return est_thematique or est_negatif
        
    # Si on n'a que la description LLM, on se fie à la thématique
    if not racines:
        return True  # pas assez d'information pour juger
        
    return est_thematique
