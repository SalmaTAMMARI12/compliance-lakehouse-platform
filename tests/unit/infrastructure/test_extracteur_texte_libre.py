"""Tests golden — prestataire d'audit, extrait du texte libre (page 4)."""

from __future__ import annotations

from dgssi_platform.infrastructure.extraction.regex.extracteur_texte_libre import (
    extraire_prestataire,
)

TEXTE_EXEMPLE = (
    "Le PASSI FFFFFF a procédé à un audit de la sécurité du système "
    "d'information DE L'AUDITÉXXX conformément à la loi 05.20..."
)


def test_extraire_prestataire_golden() -> None:
    prestataire, confiance = extraire_prestataire(TEXTE_EXEMPLE)

    assert prestataire == "PASSI FFFFFF"
    assert confiance == 0.9


def test_extraire_prestataire_absent() -> None:
    texte = "Un texte qui ne mentionne aucun prestataire d'audit."
    prestataire, confiance = extraire_prestataire(texte)

    assert prestataire is None
    assert confiance == 0.0