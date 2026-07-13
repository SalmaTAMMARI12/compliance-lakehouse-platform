"""Tests de non-régression pour la vérification d'intégrité (hash SHA-256).

Ces tests ne nécessitent PAS de connexion à un vrai MinIO : on simule
(monkeypatch) les fonctions de téléchargement pour contrôler exactement
ce que verifier_integrite_fichier() reçoit comme contenu et métadonnées.

À placer dans le dossier de tests du projet (ex: tests/infrastructure/storage/)
et lancer avec : pytest test_integrite_minio.py -v
"""
from __future__ import annotations

import pytest

from dgssi_platform.infrastructure.storage import minio_client


def test_integrite_confirmee_si_hash_identique(monkeypatch):
    """Cas nominal : le hash recalculé correspond au hash stocké -> pas d'erreur,
    la fonction retourne True."""
    contenu_bidon = b"contenu de test"
    hash_correct = minio_client.calculer_hash_sha256(contenu_bidon)

    def fake_telecharger_objet(bucket, cle):
        return contenu_bidon

    def fake_telecharger_json(bucket, cle):
        return {"content_SHA-256": hash_correct}

    monkeypatch.setattr(minio_client, "telecharger_objet", fake_telecharger_objet)
    monkeypatch.setattr(minio_client, "telecharger_json", fake_telecharger_json)

    assert minio_client.verifier_integrite_fichier("bronze", "rapport.pdf") is True


def test_integrite_leve_erreur_si_fichier_altere(monkeypatch):
    """LE cas critique à démontrer : le fichier a changé depuis son dépôt
    (contenu != hash stocké) -> ValueError, le pipeline doit s'arrêter net,
    pas continuer avec un fichier potentiellement compromis."""
    contenu_altere = b"contenu MODIFIE apres depot"
    hash_original = minio_client.calculer_hash_sha256(b"contenu original")

    def fake_telecharger_objet(bucket, cle):
        return contenu_altere

    def fake_telecharger_json(bucket, cle):
        return {"content_SHA-256": hash_original}

    monkeypatch.setattr(minio_client, "telecharger_objet", fake_telecharger_objet)
    monkeypatch.setattr(minio_client, "telecharger_json", fake_telecharger_json)

    with pytest.raises(ValueError, match="Intégrité compromise"):
        minio_client.verifier_integrite_fichier("bronze", "rapport.pdf")


def test_integrite_leve_erreur_si_metadata_absente(monkeypatch):
    """Cas limite : le fichier de métadonnées est absent ou illisible -> on ne
    doit pas continuer comme si de rien n'était (fail loud, pas fail silent)."""
    def fake_telecharger_objet(bucket, cle):
        return b"peu importe"

    def fake_telecharger_json(bucket, cle):
        raise KeyError("_metadata introuvable")

    monkeypatch.setattr(minio_client, "telecharger_objet", fake_telecharger_objet)
    monkeypatch.setattr(minio_client, "telecharger_json", fake_telecharger_json)

    with pytest.raises(KeyError):
        minio_client.verifier_integrite_fichier("bronze", "rapport.pdf")