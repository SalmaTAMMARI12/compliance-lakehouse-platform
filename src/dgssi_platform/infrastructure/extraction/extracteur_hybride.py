"""ExtracteurHybride — implémentation du port Extracteur, orchestre les
sous-extracteurs par famille de données (regex pour l'instant, NLP/LLM
viendra plus tard pour les constats en texte libre).
"""
from __future__ import annotations

from datetime import datetime

from dgssi_platform.domain.entities.audit import Audit, AuditTechnique, ChapitreAudit, VersionDocument
from dgssi_platform.domain.entities.iiv import IIV
from dgssi_platform.domain.interfaces.extracteur import Extracteur
from dgssi_platform.domain.interfaces.parseur import DocumentBrut
from dgssi_platform.infrastructure.extraction.regex.extracteur_clauses import (
    extraire_clauses_par_chapitre,
)
from dgssi_platform.infrastructure.extraction.regex.extracteur_metadonnees import (
    extraire_classification,
    extraire_historique_versions,
)
from dgssi_platform.infrastructure.extraction.regex.extracteur_tableaux_chiffres import (
    extraire_resultats_par_element,
    extraire_taux_conformite_global,
)
from dgssi_platform.infrastructure.extraction.regex.extracteur_texte_libre import (
    extraire_prestataire,
)
from dgssi_platform.infrastructure.extraction.llm.extracteur_constats import (
    extraire_non_conformites,
)
from dgssi_platform.infrastructure.referentiel.loader import (
    obtenir_noms_chapitres_ordonnes,
)
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)


def _convertir_versions(versions_brutes: list[dict[str, str]]) -> list[VersionDocument]:
    resultats: list[VersionDocument] = []
    for v in versions_brutes:
        try:
            date_parsee = datetime.strptime(v["date"], "%d/%m/%Y").date()
        except ValueError:
            logger.warning("Date de version illisible, ignorée : %s", v)
            continue
        resultats.append(
            VersionDocument(version=v["version"], date=date_parsee, commentaire=v["commentaire"])
        )
    return resultats


class ExtracteurHybride(Extracteur):
    def extraire(self, document: DocumentBrut) -> Audit:
        tableaux = document.tableaux
        texte = document.texte

        classification, conf_classif = extraire_classification(tableaux)
        historique_brut, conf_historique = extraire_historique_versions(tableaux)
        taux_global, conf_taux = extraire_taux_conformite_global(tableaux)
        resultats_element, conf_resultats = extraire_resultats_par_element(tableaux)
        prestataire, conf_prestataire = extraire_prestataire(texte)

        # Les codes DNSSI (...) sont associés aux chapitres par ordre
        # d'apparition (voir extracteur_clauses.py) : les titres Markdown
        # générés par Docling ne sont pas fiables (ex. §3.4 "Gestion des
        # actifs informationnels" n'est pas détectée comme titre).
        noms_chapitres = obtenir_noms_chapitres_ordonnes()
        clauses_par_chapitre, conf_clauses = extraire_clauses_par_chapitre(texte, noms_chapitres)

        non_conformites, conf_llm = extraire_non_conformites(texte, clauses_par_chapitre)

        historique = _convertir_versions(historique_brut)
        audit_technique = (
            AuditTechnique(resultats_par_element=resultats_element)
            if resultats_element
            else None
        )

        # ChapitreAudit.objectifs / notes_audit non extraits ici (texte libre,
        # relève d'un extracteur NLP/LLM futur) — initialisés vides plutôt que
        # bloquer la validation Pydantic. Seul .clauses est fiable à ce stade.
        chapitres = [
            ChapitreAudit(nom_chapitre=nom, clauses=codes, objectifs="", notes_audit="")
            for nom, codes in clauses_par_chapitre.items()
        ]

        confiances = [
            conf_classif, conf_historique, conf_taux, conf_resultats, conf_prestataire, conf_clauses, conf_llm,
        ]
        confiance_moyenne = sum(confiances) / len(confiances)
        logger.info(
            "Extraction terminée — confiance moyenne: %.2f "
            "(classif=%.2f, historique=%.2f, taux=%.2f, résultats=%.2f, prestataire=%.2f, clauses=%.2f)",
            confiance_moyenne, conf_classif, conf_historique, conf_taux, conf_resultats,
            conf_prestataire, conf_clauses,
        )

        return Audit(
            iiv=IIV(nom="IIV_A", secteur="inconnu"),
            classification=classification or "INCONNUE",
            historique_versions=historique,
            prestataire_audit=prestataire or "INCONNU",
            taux_conformite_global=taux_global,
            audit_technique=audit_technique,
            chapitres=chapitres,
            non_conformites=non_conformites,
            confiance_extraction={
                "classif": conf_classif,
                "historique": conf_historique,
                "taux": conf_taux,
                "resultats": conf_resultats,
                "prestataire": conf_prestataire,
                "clauses": conf_clauses,
                "llm": conf_llm,
            },
        )