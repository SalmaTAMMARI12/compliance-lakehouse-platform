"""Variante de traiter() qui réutilise le Silver déjà écrit — SAUTE
Docling entièrement. Sert à valider le reste du pipeline (dédup par hash,
extraction, Gold, Postgres) sans dépendre du fix mémoire Docling, pas
encore confirmé stable sur cette machine.

Le hash de dédup reste calculé sur le PDF Bronze original (pas sur le
Silver) — c'est le contenu du PDF qui définit l'identité du rapport, pas
sa représentation Markdown.
"""
from __future__ import annotations

import hashlib
import json
import sys

from dgssi_platform.domain.interfaces.parseur import DocumentBrut
from dgssi_platform.domain.services.calculer_taux_conformite import (
    calculer_couverture_referentiel,
)
from dgssi_platform.domain.services.moteur_conformite import (
    classer_elements_par_exposition,
    compter_ecarts_critiques,
    evaluer_conformite_globale,
)
from dgssi_platform.domain.services.validateur_audit import valider_audit
from dgssi_platform.infrastructure.database.repositories.audit_repository import (
    sauvegarder_audit,
    trouver_audit_par_hash,
)
from dgssi_platform.infrastructure.database.repositories.conformite_repository import (
    sauvegarder_evaluation,
)
from dgssi_platform.infrastructure.extraction.extracteur_hybride import ExtracteurHybride
from dgssi_platform.infrastructure.referentiel.loader import obtenir_exigences
from dgssi_platform.infrastructure.storage.minio_client import (
    telecharger_objet,
    upload_json,
    verifier_integrite_fichier,
)
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def traiter_depuis_silver(nom_fichier_bronze: str) -> None:
    verifier_integrite_fichier("bronze", nom_fichier_bronze)
    contenu_bronze = telecharger_objet("bronze", nom_fichier_bronze)
    hash_contenu = hashlib.sha256(contenu_bronze).hexdigest()

    audit_existant_id = trouver_audit_par_hash(hash_contenu)
    if audit_existant_id is not None:
        print(f"Ce rapport a déjà été traité (audit id={audit_existant_id}). Aucune action effectuée.")
        return

    nom_document = nom_fichier_bronze.rsplit(".", 1)[0]
    prefixe = f"{nom_document}/"

    texte = telecharger_objet("silver", f"{prefixe}texte.md").decode("utf-8")
    tableaux = json.loads(telecharger_objet("silver", f"{prefixe}tableaux.json").decode("utf-8"))
    document = DocumentBrut(texte=texte, tableaux=tableaux, nb_pages=40)
    logger.info("Silver réutilisé (Docling SAUTÉ) : %d caractères, %d tableaux", len(texte), len(tableaux))

    audit = ExtracteurHybride().extraire(document)

    erreurs_validation = valider_audit(audit)
    if erreurs_validation:
        logger.warning("Audit extrait avec des incohérences : %s", erreurs_validation)

    exigences = obtenir_exigences()
    couverture = calculer_couverture_referentiel(audit, exigences)

    upload_json("gold", f"{nom_document}.json", audit.model_dump())

    audit_id = sauvegarder_audit(audit, confiance_extraction=0.96, hash_sha256=hash_contenu)

    evaluation = evaluer_conformite_globale(audit)
    classement = classer_elements_par_exposition(audit)
    nb_critiques = compter_ecarts_critiques(audit)
    element_expose = classement[0]["element"] if classement else "AUCUN"

    eval_id = sauvegarder_evaluation(
        audit_id=audit_id,
        statut=evaluation["statut"],
        seuil=evaluation["seuil"],
        nb_ecarts_critiques=nb_critiques,
        element_le_plus_expose=element_expose,
    )

    print("=" * 60)
    print(f"Traitement terminé (Docling SAUTÉ) pour : {nom_fichier_bronze}")
    print(f"  Audit id (Postgres)      : {audit_id}")
    print(f"  Évaluation id            : {eval_id}")
    print(f"  Statut                   : {evaluation['statut']}")
    print(f"  Taux de conformité       : {audit.taux_conformite_global}%")
    print(f"  Non-conformités          : {len(audit.non_conformites)}")
    print(f"  Couverture référentiel   : {couverture['taux_couverture_referentiel']}%")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python traiter_depuis_silver.py <nom_fichier_dans_bronze>")
        sys.exit(1)
    traiter_depuis_silver(sys.argv[1])