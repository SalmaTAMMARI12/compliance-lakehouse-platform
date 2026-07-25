"""Entité NonConformite — résultat structuré d'un constat en texte libre,
produit par extraction LLM (infrastructure/extraction/llm/).

Le champ 'type' (significatif/non_significatif/remarque) a été retiré
volontairement : cette information n'est pas présente au niveau de chaque
constat individuel dans le rapport source (seuls des totaux agrégés le
sont — voir section 2.3 du rapport de référence). L'extraire reviendrait
à l'inventer, que ce soit via Regex ou LLM. Si les "fiches d'écarts"
séparées mentionnées dans le rapport deviennent disponibles un jour, ce
champ pourra être réintroduit via un extracteur Regex dédié.

texte_source et methode_extraction assurent la traçabilité exigée par la
gouvernance de données : on doit toujours pouvoir remonter à la phrase
d'origine et savoir si une donnée vient d'une règle déterministe ou d'un
enrichissement LLM.
"""
from __future__ import annotations

from pydantic import BaseModel


class NonConformite(BaseModel):
    chapitre: str
    texte_source: str
    resume_constat: str
    recommandation: str | None = None
    actifs_concernes: list[str] = []
    echeance: str | None = None
    confiance: float = 0.0
    methode_extraction: str = "llm"
    a_verifier: bool = False
    est_note: bool = False
