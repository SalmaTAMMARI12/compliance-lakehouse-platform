"""Port : Extracteur — extrait les informations de conformité depuis un DocumentBrut."""

from __future__ import annotations

from abc import ABC, abstractmethod

from dgssi_platform.domain.entities.audit import Audit
from dgssi_platform.domain.interfaces.parseur import DocumentBrut


class Extracteur(ABC):
    """Toute technique d'extraction métier (regex, NLP, futur LLM) implémente ce port."""

    @abstractmethod
    def extraire(self, document: DocumentBrut) -> Audit:
        raise NotImplementedError