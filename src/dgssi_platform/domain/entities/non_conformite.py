"""Entité NonConformite — résultat structuré d'un constat en texte libre,
produit par extraction LLM (infrastructure/extraction/llm/). Distincte des
clauses DNSSI (codes techniques) : ici on capture le VERDICT rédigé en
prose par l'auditeur, reformulé de façon structurée.

Le champ a_verifier signale une incohérence détectée entre le chapitre
attendu et le contenu extrait — cas connu où Docling associe mal le texte
au bon chapitre sur les tableaux multi-pages de ce type de rapport. Un
résultat marqué a_verifier=True reste utilisable mais doit être relu par
un humain avant d'être considéré fiable en base.
"""
from __future__ import annotations

from pydantic import BaseModel


class NonConformite(BaseModel):
    chapitre: str
    type: str  # "significatif" | "non_significatif" | "remarque"
    description: str
    recommandation: str | None = None
    a_verifier: bool = False
