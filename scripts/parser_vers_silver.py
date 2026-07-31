"""OUTIL DE DEBUG UNIQUEMENT — ne fait PAS partie du pipeline de production.

Teste isolément la brique Parseur → Silver sur un fichier LOCAL, sans
passer par Bronze/MinIO. Utile pour déboguer un problème de parsing sur
un PDF/DOCX sans relancer tout le pipeline.

Sélection automatique du parseur :
  - .docx → DocxParseur (python-docx, 10x plus rapide, zéro rich cells)
  - .pdf  → DoclingParseur (Docling, avec la nouvelle API doc= corrigée)

Le vrai pipeline de production est scripts/executer_pipeline_complet.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dgssi_platform.infrastructure.storage.minio_client import upload_json, upload_texte
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def _choisir_parseur(chemin: Path):
    """Retourne le parseur adapté à l'extension du fichier."""
    ext = chemin.suffix.lower()
    if ext in (".docx", ".doc"):
        from dgssi_platform.infrastructure.parsing.office.docx_parseur import DocxParseur
        logger.info("Format DOCX detecte — utilisation de DocxParseur (python-docx)")
        return DocxParseur()
    elif ext == ".pdf":
        from dgssi_platform.infrastructure.parsing.docling.docling_parseur import DoclingParseur
        logger.info("Format PDF detecte — utilisation de DoclingParseur (Docling)")
        return DoclingParseur()
    else:
        raise ValueError(f"Format non supporte : '{ext}'. Fichiers acceptes : .pdf, .docx")


def parser_et_uploader(chemin_local: Path) -> None:
    nom_sans_extension = chemin_local.stem
    parseur = _choisir_parseur(chemin_local)
    document = parseur.parser(chemin_local)
    prefixe = f"{nom_sans_extension}/"
    upload_texte("silver", f"{prefixe}texte.md", document.texte)
    upload_json("silver", f"{prefixe}tableaux.json", document.tableaux)
    logger.info(
        "[DEBUG] Termine : %d pages, %d tableaux ecrits dans silver/%s",
        document.nb_pages or 0,
        len(document.tableaux),
        prefixe,
    )
    print(f"\nOK — silver/{prefixe}texte.md et tableaux.json mis a jour")
    print(f"     {len(document.tableaux)} tableaux, {len(document.texte)} caracteres de texte")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage (DEBUG UNIQUEMENT): python parser_vers_silver.py <chemin_local_du_fichier>")
        print("  Formats supportes : .pdf, .docx")
        sys.exit(1)
    parser_et_uploader(Path(sys.argv[1]))
