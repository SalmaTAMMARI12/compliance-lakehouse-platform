"""Pipeline complet : Bronze (vérif intégrité + dédup par hash) → Docling
→ Silver → ExtracteurHybride (Regex + LLM) → Gold (MinIO) → Postgres →
Moteur de conformité.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

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
from dgssi_platform.infrastructure.parsing.docling.docling_parseur import DoclingParseur
from dgssi_platform.infrastructure.referentiel.loader import obtenir_exigences
from dgssi_platform.infrastructure.storage.minio_client import (
    telecharger_objet,
    upload_json,
    upload_texte,
    verifier_integrite_fichier,
)
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def traiter(nom_fichier_bronze: str) -> None:
    # 1. Intégrité — bloque si le fichier a été altéré depuis son dépôt
    verifier_integrite_fichier("bronze", nom_fichier_bronze)

    # 2. Téléchargement + dédup par hash de contenu — AVANT tout traitement
    #    coûteux (Docling, LLM), pour ne jamais retraiter un doublon exact.
    contenu = telecharger_objet("bronze", nom_fichier_bronze)
    hash_contenu = hashlib.sha256(contenu).hexdigest()

    audit_existant_id = trouver_audit_par_hash(hash_contenu)
    if audit_existant_id is not None:
        logger.info(
            "Rapport déjà traité (hash identique) — audit id=%d existant, aucun retraitement.",
            audit_existant_id,
        )
        print(f"Ce rapport a déjà été traité (audit id={audit_existant_id}). Aucune action effectuée.")
        return

    # 3. Parsing Docling — fonctionne sur un fichier LOCAL
    chemin_temp = Path(f"_temp_{nom_fichier_bronze}")
    chemin_temp.write_bytes(contenu)

    try:
        document = DoclingParseur().parser(chemin_temp)
    finally:
        chemin_temp.unlink(missing_ok=True)

    nom_document = Path(nom_fichier_bronze).stem
    prefixe = f"{nom_document}/"

    # 4. Écriture Silver
    upload_texte("silver", f"{prefixe}texte.md", document.texte)
    upload_json("silver", f"{prefixe}tableaux.json", document.tableaux)
    logger.info("Silver écrit : %d pages, %d tableaux", document.nb_pages, len(document.tableaux))

    # 5. Extraction
    audit = ExtracteurHybride().extraire(document)

    erreurs_validation = valider_audit(audit)
    if erreurs_validation:
        logger.warning("Audit extrait avec des incohérences : %s", erreurs_validation)

    # 5bis. Couverture référentiel
    exigences = obtenir_exigences()
    couverture = calculer_couverture_referentiel(audit, exigences)
    logger.info(
        "Couverture référentiel : %s%% (%d/%d exigences couvertes)",
        couverture["taux_couverture_referentiel"],
        couverture["nb_exigences_couvertes"],
        couverture["nb_exigences_attendues"],
    )

    # 6. Gold
    upload_json("gold", f"{nom_document}.json", audit.model_dump())
    logger.info("Gold écrit : gold/%s.json", nom_document)

    # 7. Postgres
    audit_id = sauvegarder_audit(audit, confiance_extraction=0.96, hash_sha256=hash_contenu)
    logger.info("Audit sauvegardé en base, id=%d", audit_id)

    # 8. Moteur de conformité
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
    print(f"Traitement terminé pour : {nom_fichier_bronze}")
    print(f"  Audit id (Postgres)      : {audit_id}")
    print(f"  Évaluation id            : {eval_id}")
    print(f"  Statut                   : {evaluation['statut']}")
    print(f"  Taux de conformité       : {audit.taux_conformite_global}%")
    print(f"  Écarts critiques         : {nb_critiques}")
    print(f"  Élément le plus exposé   : {element_expose}")
    print(f"  Couverture référentiel   : {couverture['taux_couverture_referentiel']}% ({couverture['nb_exigences_couvertes']}/{couverture['nb_exigences_attendues']})")
    print(f"  Erreurs de validation    : {erreurs_validation or 'AUCUNE'}")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extraire_audit_depuis_silver.py <nom_fichier_dans_bronze>")
        sys.exit(1)
    traiter(sys.argv[1])