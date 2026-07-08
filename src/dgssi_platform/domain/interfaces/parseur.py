"""Port : Parseur — transforme un fichier brut en contenu structurable, sans interprétation métier."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import BaseModel


class DocumentBrut(BaseModel):
    """Sortie neutre du parsing : texte, tableaux, images — pas encore de sens métier."""

    texte: str
    tableaux: list[list[list[str]]] = []
    nb_pages: int | None = None


class Parseur(ABC):
    """Toute source (PDF, Word, Excel, PDF scanné) doit implémenter ce port."""

    @abstractmethod
    def parser(self, chemin_fichier: Path) -> DocumentBrut:
        raise NotImplementedError