import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dgssi_platform.infrastructure.database.session import SessionLocal
from dgssi_platform.infrastructure.database.models.audit_model import AuditModel
from dgssi_platform.infrastructure.storage.minio_client import telecharger_json
from dgssi_platform.domain.entities.audit import Audit
from dgssi_platform.infrastructure.database.repositories.audit_repository import sauvegarder_audit
from dgssi_platform.infrastructure.database.repositories.conformite_repository import sauvegarder_evaluation
from dgssi_platform.domain.services.moteur_conformite import evaluer_conformite_globale, classer_elements_par_exposition, compter_ecarts_critiques

from sqlalchemy import text

def re_sauvegarder():
    session = SessionLocal()
    session.execute(text("TRUNCATE TABLE audits CASCADE;"))
    session.commit()
    print("Anciens audits supprimés de la BD.")
    session.close()

    for nom_rapport in ["Exemple de rapport d'audit", "Rapport-Audit-Sécurité-Organisationnelle_DNSSI1"]:
        try:
            data = telecharger_json("gold", f"{nom_rapport}.json")
            audit = Audit(**data)
            
            audit_id = sauvegarder_audit(
                audit, 
                confiance_extraction=0.92,
                hash_sha256=nom_rapport,
            )

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
            print(f"Sauvegardé avec succès: {nom_rapport}")
        except Exception as e:
            print(f"Erreur pour {nom_rapport}: {e}")

if __name__ == '__main__':
    re_sauvegarder()
