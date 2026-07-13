"""Implémentation du port Parseur avec Docling.

Vérifie explicitement le statut de conversion : Docling peut échouer
partiellement (pages non traitées, ex. std::bad_alloc sous contrainte
mémoire) sans lever d'exception native — dans ce cas on refuse de retourner
un texte incomplet en silence, on lève ErreurParsing à la place.

Vérifie aussi, indépendamment du statut déclaré par Docling, que le nombre
de pages effectivement traitées correspond au nombre de pages réel du PDF
source (compté via pypdf) — pour ne pas dépendre uniquement du jugement
que Docling porte sur sa propre réussite.
"""

from __future__ import annotations

from pathlib import Path

from docling.datamodel.base_models import ConversionStatus, InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from pypdf import PdfReader

from dgssi_platform.domain.exceptions import ErreurParsing
from dgssi_platform.domain.interfaces.parseur import DocumentBrut, Parseur
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


class DoclingParseur(Parseur):
    def __init__(self) -> None:
        options = PdfPipelineOptions()
        options.do_ocr = False

        self._converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)}
        )

    def parser(self, chemin_fichier: Path) -> DocumentBrut:
        logger.info("Parsing de %s avec Docling", chemin_fichier.name)
        resultat = self._converter.convert(str(chemin_fichier))

        if resultat.status != ConversionStatus.SUCCESS:
            messages_erreur = [str(e) for e in resultat.errors]
            logger.error(
                "Parsing incomplet de %s (statut=%s) : %s",
                chemin_fichier.name,
                resultat.status,
                messages_erreur,
            )
            raise ErreurParsing(
                f"Parsing incomplet de {chemin_fichier.name} "
                f"(statut={resultat.status}) : {messages_erreur}"
            )

        document = resultat.document

        # Vérification indépendante : on ne fait pas confiance uniquement
        # au statut déclaré par Docling. On compte les pages du PDF source
        # nous-mêmes (avec pypdf, pas Docling) et on compare.
        nb_pages_source = len(PdfReader(str(chemin_fichier)).pages)
        nb_pages_traitees = len(document.pages) if document.pages else 0

        if nb_pages_traitees != nb_pages_source:
            logger.error(
                "Incohérence de pages pour %s : source=%d, Docling a traité=%d "
                "(statut déclaré=%s)",
                chemin_fichier.name,
                nb_pages_source,
                nb_pages_traitees,
                resultat.status,
            )
            raise ErreurParsing(
                f"Incohérence de pages pour {chemin_fichier.name} : le PDF "
                f"source contient {nb_pages_source} pages mais Docling n'en "
                f"a traité que {nb_pages_traitees}, malgré un statut déclaré "
                f"'{resultat.status}'."
            )

        texte = document.export_to_markdown()
        tableaux = [
            table.export_to_dataframe().values.tolist()
            for table in document.tables
        ]

        return DocumentBrut(
            texte=texte,
            tableaux=tableaux,
            nb_pages=nb_pages_traitees,
        )