"""Classification du type d'un écart (significatif / non_significatif /
remarque) par mots-clés sur le texte source brut. Volontairement en Regex
plutôt que via le LLM : les tests ont montré que Qwen2.5-1.5B n'appliquait
pas cette règle de façon fiable, alors que la détection par mots-clés est
prévisible et vérifiée sur les cas réels du rapport de référence.
"""

from __future__ import annotations

TYPES_VALIDES = {"significatif", "non_significatif", "remarque"}

_MARQUEURS_ABSENCE = [
    "absence de", "absence d'", "aucun", "aucune",
    "n'est pas", "ne dispose pas", "non conforme",
]
_MARQUEURS_EN_COURS = [
    "en cours de validation", "en cours d'instauration",
    "en cours de finalisation", "en cours de réalisation",
]
_MARQUEURS_PLANIFIE = [
    "planifié", "prévu pour", "sera", "procèdera", "à l'issue de",
]


def classifier_type_ecart(texte_constat: str) -> str:
    texte = texte_constat.lower()
    if any(m in texte for m in _MARQUEURS_ABSENCE):
        return "significatif"
    if any(m in texte for m in _MARQUEURS_EN_COURS):
        return "non_significatif"
    if any(m in texte for m in _MARQUEURS_PLANIFIE):
        return "remarque"
    return "non_significatif"
