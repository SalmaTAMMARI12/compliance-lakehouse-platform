"""
Pipeline complet DGSSI — Silver -> Extraction -> Gold + PostgreSQL.

Contourne volontairement Docling (source du crash RAM sur les rapports de
40+ pages) : lit directement le texte et les tableaux déjà déposés dans
Silver par une étape antérieure, au lieu de re-parser le PDF.

Usage :
    venv/Scripts/python scripts/executer_pipeline_complet.py "Exemple de rapport d'audit"

Le nom passé en argument doit correspondre au préfixe du dossier dans le
bucket Silver (silver/<nom>/texte.md et silver/<nom>/tableaux.json).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dgssi_platform.domain.interfaces.parseur import DocumentBrut
from dgssi_platform.domain.services.moteur_conformite import (
    classer_elements_par_exposition,
    compter_ecarts_critiques,
    evaluer_conformite_globale,
)
from dgssi_platform.infrastructure.database.repositories.audit_repository import sauvegarder_audit
from dgssi_platform.infrastructure.database.repositories.conformite_repository import sauvegarder_evaluation
from dgssi_platform.infrastructure.extraction.extracteur_hybride import ExtracteurHybride
from dgssi_platform.infrastructure.storage.minio_client import telecharger_objet, upload_json
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def executer(nom_rapport: str, confiance_extraction_defaut: float = 0.92) -> int:
    """Retourne 0 si succès, 1 si échec — pour un exit code exploitable en script."""

    print(f"{'='*60}")
    print(f"Pipeline DGSSI — rapport : {nom_rapport}")
    print(f"{'='*60}\n")

    # --- Étape 1 : lecture depuis Silver (pas de Docling, pas de RAM) ---
    try:
        print("[1/4] Lecture depuis Silver...")
        texte = telecharger_objet("silver", f"{nom_rapport}/texte.md").decode("utf-8")
        tableaux = json.loads(
            telecharger_objet("silver", f"{nom_rapport}/tableaux.json").decode("utf-8")
        )
        print(f"      OK — texte: {len(texte)} caractères, {len(tableaux)} tableaux")
    except Exception as e:
        print(f"      ÉCHEC — impossible de lire Silver : {e}")
        print("      Vérifiez que le dossier existe : silver/{}/texte.md et tableaux.json".format(nom_rapport))
        return 1

    # --- Étape 2 : extraction (regex + LLM) ---
    try:
        print("\n[2/4] Extraction (regex + LLM local, patientez — plusieurs minutes)...")
        document = DocumentBrut(texte=texte, tableaux=tableaux, nb_pages=0)
        audit = ExtracteurHybride().extraire(document)
        print(f"      OK — taux: {audit.taux_conformite_global}% | "
              f"chapitres: {len(audit.chapitres)} | "
              f"non-conformités: {len(audit.non_conformites)}")
    except Exception as e:
        print(f"      ÉCHEC — extraction interrompue : {e}")
        print("      Le modèle LLM est-il bien téléchargé et le chemin correct dans client_llm.py ?")
        return 1

    # --- Étape 3 : sauvegarde Gold (MinIO) ---
    try:
        print("\n[3/4] Sauvegarde Gold (MinIO)...")
        upload_json("gold", f"{nom_rapport}.json", audit.model_dump())
        print(f"      OK — gold/{nom_rapport}.json mis à jour")
    except Exception as e:
        print(f"      ÉCHEC — sauvegarde Gold impossible : {e}")
        return 1

    # --- Étape 4 : sauvegarde PostgreSQL ---
    try:
        print("\n[4/4] Sauvegarde PostgreSQL...")
        audit_id = sauvegarder_audit(audit, confiance_extraction=confiance_extraction_defaut)

        evaluation = evaluer_conformite_globale(audit)
        classement = classer_elements_par_exposition(audit)
        nb_critiques = compter_ecarts_critiques(audit)
        element_expose = classement[0]["element"] if classement else "AUCUN"

        sauvegarder_evaluation(
            audit_id=audit_id,
            statut=evaluation["statut"],
            seuil=evaluation["seuil"],
            nb_ecarts_critiques=nb_critiques,
            element_le_plus_expose=element_expose,
        )
        print(f"      OK — audit_id={audit_id}")
    except Exception as e:
        print(f"      ÉCHEC — sauvegarde PostgreSQL impossible : {e}")
        print("      Vérifiez que le conteneur dgssi-postgres tourne (docker ps).")
        return 1

    print(f"\n{'='*60}")
    print("RÉSUMÉ")
    print(f"{'='*60}")
    print(f"Audit id            : {audit_id}")
    print(f"Statut               : {evaluation['statut']}")
    print(f"Taux de conformité   : {audit.taux_conformite_global}%")
    print(f"Écarts critiques     : {nb_critiques}")
    print(f"Élément le plus exposé : {element_expose}")
    print(f"Non-conformités      : {len(audit.non_conformites)}")
    print(f"{'='*60}")
    print("\nPipeline terminé avec succès. Rafraîchissez le dashboard pour voir ce nouvel audit.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "nom_rapport",
        help="Nom du rapport tel qu'utilisé comme préfixe de dossier dans Silver "
             "(ex. 'Exemple de rapport d'audit')",
    )
    parser.add_argument(
        "--confiance",
        type=float,
        default=0.92,
        help="Confiance d'extraction par défaut à enregistrer (0.0-1.0)",
    )
    args = parser.parse_args()

    code_sortie = executer(args.nom_rapport, args.confiance)
    sys.exit(code_sortie)