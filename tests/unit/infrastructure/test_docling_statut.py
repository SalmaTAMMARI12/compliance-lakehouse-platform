"""Tests de non-régression : DoclingParseur doit refuser un parsing
incomplet (PARTIAL_SUCCESS / FAILURE) plutôt que retourner un texte tronqué
en silence.

On ne fait PAS tourner le vrai Docling ici (trop lent, charge des modèles
ML à chaque test) : on simule le convertisseur interne (_converter) pour
contrôler précisément le statut retourné, sans dépendre du PDF réel.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from docling.datamodel.base_models import ConversionStatus

from dgssi_platform.domain.exceptions import ErreurParsing
from dgssi_platform.infrastructure.parsing.docling.docling_parseur import DoclingParseur


def _construire_parseur_avec_convertisseur_bidon(resultat_simule):
    """Construit un DoclingParseur SANS passer par __init__ (qui charge les
    vrais modèles Docling, ~10s), et lui injecte un faux convertisseur dont
    on contrôle entièrement le résultat."""
    parseur = object.__new__(DoclingParseur)
    parseur._converter = MagicMock()
    parseur._converter.convert.return_value = resultat_simule
    return parseur


def test_parsing_reussi_retourne_document(tmp_path):
    """Cas nominal : statut SUCCESS -> le document est retourné normalement."""
    faux_document = MagicMock()
    faux_document.export_to_markdown.return_value = "# Texte extrait"
    faux_document.tables = []
    faux_document.pages = {1: object(), 2: object()}

    resultat_simule = MagicMock()
    resultat_simule.status = ConversionStatus.SUCCESS
    resultat_simule.document = faux_document

    parseur = _construire_parseur_avec_convertisseur_bidon(resultat_simule)
    chemin_bidon = tmp_path / "test.pdf"
    chemin_bidon.write_bytes(b"%PDF-1.4 contenu bidon")

    with patch(
        "dgssi_platform.infrastructure.parsing.docling.docling_parseur.PdfReader"
    ) as mock_pdf_reader:
        mock_pdf_reader.return_value.pages = [MagicMock(), MagicMock()]

        document = parseur.parser(chemin_bidon)

    assert document.texte == "# Texte extrait"
    assert document.nb_pages == 2


def test_parsing_partiel_leve_erreur_parsing(tmp_path):
    """LE cas important à démontrer : si Docling ne réussit qu'à moitié
    (ex. manque de mémoire sur une page -> std::bad_alloc), on doit lever
    ErreurParsing, PAS retourner un texte tronqué silencieusement."""
    resultat_simule = MagicMock()
    resultat_simule.status = ConversionStatus.PARTIAL_SUCCESS
    resultat_simule.errors = ["std::bad_alloc sur la page 12"]

    parseur = _construire_parseur_avec_convertisseur_bidon(resultat_simule)
    chemin_bidon = tmp_path / "test.pdf"
    chemin_bidon.write_bytes(b"%PDF-1.4 contenu bidon")

    with pytest.raises(ErreurParsing, match="Parsing incomplet"):
        parseur.parser(chemin_bidon)


def test_parsing_echec_total_leve_erreur_parsing(tmp_path):
    """Cas d'échec complet (FAILURE) : même logique de refus."""
    resultat_simule = MagicMock()
    resultat_simule.status = ConversionStatus.FAILURE
    resultat_simule.errors = ["fichier corrompu"]

    parseur = _construire_parseur_avec_convertisseur_bidon(resultat_simule)
    chemin_bidon = tmp_path / "test.pdf"
    chemin_bidon.write_bytes(b"%PDF-1.4 contenu bidon")

    with pytest.raises(ErreurParsing):
        parseur.parser(chemin_bidon)