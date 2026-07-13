from __future__ import annotations

from dgssi_platform.domain.entities.audit import Audit
from dgssi_platform.infrastructure.database.models.audit_model import (
    AuditModel,
    HistoriqueVersionModel,
    ResultatTechniqueModel,
)
from dgssi_platform.infrastructure.database.session import get_session


def sauvegarder_audit(audit: Audit, confiance_extraction: float) -> int:
    with get_session() as session:
        existant = (
            session.query(AuditModel)
            .filter_by(
                iiv_nom=audit.iiv.nom,
                prestataire_audit=audit.prestataire_audit,
                taux_conformite_global=audit.taux_conformite_global,
            )
            .first()
        )
        if existant:
            return existant.id  # déjà en base, on ne duplique pas

        modele = AuditModel(
            iiv_nom=audit.iiv.nom,
            iiv_secteur=audit.iiv.secteur,
            prestataire_audit=audit.prestataire_audit,
            classification=audit.classification,
            taux_conformite_global=audit.taux_conformite_global,
            confiance_extraction=confiance_extraction,
        )
        for v in audit.historique_versions:
            modele.historique_versions.append(
                HistoriqueVersionModel(version=v.version, date=v.date, commentaire=v.commentaire)
            )
        if audit.audit_technique:
            for element, valeurs in audit.audit_technique.resultats_par_element.items():
                modele.resultats_techniques.append(
                    ResultatTechniqueModel(
                        element_audite=element,
                        critique=valeurs["CRITIQUE"],
                        elevee=valeurs["ELEVEE"],
                        moyenne=valeurs["MOYENNE"],
                        faible=valeurs["FAIBLE"],
                    )
                )

        session.add(modele)
        session.commit()
        return modele.id