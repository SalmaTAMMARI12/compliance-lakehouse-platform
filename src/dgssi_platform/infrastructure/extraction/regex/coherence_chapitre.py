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


def est_coherent_avec_chapitre(description: str, codes_dnssi: list[str]) -> bool:
    """Retourne True si la description semble appartenir au bon chapitre,
    False si aucun signal thématique ne correspond (à vérifier manuellement)."""
    racines = _extraire_racines_thematiques(codes_dnssi)
    if not racines:
        return True  # pas assez d'information pour juger, on ne bloque pas

    texte = description.lower()
    return any(racine in texte for racine in racines)
