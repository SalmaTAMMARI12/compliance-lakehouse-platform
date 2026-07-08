"""Script manuel : parse un fichier depuis Bronze avec Docling, écrit le
résultat (texte + tableaux) dans Silver. Pas encore automatisé (Airflow
viendra plus tard) — appelé à la main pour l'instant, cohérent avec
l'approche incrémentale du projet.
"""

from __future__ import annotations

import sys
from pathlib import Path

from dgssi_platform.infrastructure.parsing.docling.docling_parseur import DoclingParseur
from dgssi_platform.infrastructure.storage.minio_client import upload_json, upload_texte
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def parser_et_uploader(chemin_local: Path) -> None:
    nom_sans_extension = chemin_local.stem

    parseur = DoclingParseur()
    document = parseur.parser(chemin_local)

    prefixe = f"{nom_sans_extension}/"
    upload_texte("silver", f"{prefixe}texte.md", document.texte)
    upload_json("silver", f"{prefixe}tableaux.json", document.tableaux)

    logger.info(
        "Terminé : %d pages, %d tableaux écrits dans silver/%s",
        document.nb_pages,
        len(document.tableaux),
        prefixe,
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser_vers_silver.py <chemin_du_fichier>")
        sys.exit(1)

    parser_et_uploader(Path(sys.argv[1]))