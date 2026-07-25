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
from dgssi_platform.infrastructure.extraction.regex.extracteur_notes_audit import (
    extraire_notes_audit_par_chapitre,
)
from dgssi_platform.infrastructure.extraction.llm.synthetiseur_notes import (
    synthetiser_notes_chapitre,
)
from dgssi_platform.infrastructure.referentiel.loader import (
    obtenir_noms_chapitres_ordonnes,
)
from dgssi_platform.shared.logging import get_logger
from dgssi_platform.infrastructure.extraction.regex.extracteur_totaux_ecarts import extraire_totaux_ecarts
from dgssi_platform.infrastructure.extraction.regex.extracteur_perimetre import extraire_perimetre_fonctionnel, extraire_perimetre_technique
from dgssi_platform.infrastructure.extraction.regex.extracteur_technique_details import extraire_referentiels_utilises, extraire_vulnerabilites_par_categorie

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

        # Regroupement par chapitre — permet de peupler ChapitreAudit.constats
        # en plus de la liste à plat Audit.non_conformites. Les deux
        # contiennent les mêmes objets (traçabilité + lecture par chapitre
        # pour le reporting), ce n'est pas une duplication de données, juste
        # deux vues sur la même source.
        non_conformites_par_chapitre: dict[str, list] = {}
        for nc in non_conformites:
            non_conformites_par_chapitre.setdefault(nc.chapitre, []).append(nc)

        historique = _convertir_versions(historique_brut)
        perimetre_fonctionnel, conf_perim_fonc = extraire_perimetre_fonctionnel(texte)
        perimetre_technique, conf_perim_tech = extraire_perimetre_technique(texte)
        referentiels_utilises, conf_ref = extraire_referentiels_utilises(texte)
        vulnerabilites, conf_vuln = extraire_vulnerabilites_par_categorie(texte)
        audit_technique = (
            AuditTechnique(
                resultats_par_element=resultats_element,
                perimetre_technique=perimetre_technique,
                referentiels_utilises=referentiels_utilises,
                points_amelioration_par_categorie=vulnerabilites,
            )
            if resultats_element
            else None
        )

        noms_chapitres = list(clauses_par_chapitre.keys())
        resultats_notes_brutes = extraire_notes_audit_par_chapitre(texte, noms_chapitres)

        chapitres = []
        conf_notes_list = []

        for nom, codes in clauses_par_chapitre.items():
            texte_brut, conf_regex = resultats_notes_brutes.get(nom, ("", 0.0))
            if texte_brut:
                conf_notes_list.append(conf_regex)

            synthese = None
            if texte_brut:
                synthese, conf_llm_notes = synthetiser_notes_chapitre(nom, texte_brut)
                conf_notes_list.append(conf_llm_notes)

            chapitres.append(
                ChapitreAudit(
                    nom_chapitre=nom,
                    clauses=codes,
                    objectifs="",
                    notes_audit=texte_brut,
                    notes_audit_synthese=synthese,
                    constats=[
                        nc.resume_constat
                        for nc in non_conformites_par_chapitre.get(nom, [])
                    ],
                )
            )

        conf_notes_avg = sum(conf_notes_list) / len(conf_notes_list) if conf_notes_list else 1.0

        confiances = [
            conf_classif, conf_historique, conf_taux, conf_resultats, conf_prestataire, conf_clauses, conf_llm, conf_notes_avg
        ]
        confiance_moyenne = sum(confiances) / len(confiances)
        logger.info(
            "Extraction terminée — confiance moyenne: %.2f "
            "(classif=%.2f, historique=%.2f, taux=%.2f, résultats=%.2f, prestataire=%.2f, clauses=%.2f)",
            confiance_moyenne, conf_classif, conf_historique, conf_taux, conf_resultats,
            conf_prestataire, conf_clauses,
        )

        totaux_ecarts, conf_totaux = extraire_totaux_ecarts(texte)

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
                "totaux_ecarts": conf_totaux,
            },
            nb_ecarts_par_type=totaux_ecarts,
            perimetre_fonctionnel=perimetre_fonctionnel,
        )