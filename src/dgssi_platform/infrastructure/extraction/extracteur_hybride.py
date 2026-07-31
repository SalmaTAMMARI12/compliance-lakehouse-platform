"""ExtracteurHybride — implémentation du port Extracteur, orchestre les
sous-extracteurs par famille de données :
- Regex pour les données structurées (codes DNSSI, versions, dates)
- LLM (Qwen) pour le contenu sémantique (scores, constats, synthèses, prestataire)

Stratégie LLM-first pour les scores et le prestataire : le LLM est appelé
en premier car chaque prestataire d'audit utilise sa propre notation.
Fallback regex si le LLM échoue.
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
from dgssi_platform.infrastructure.extraction.regex.extracteur_clauses_tableaux import (
    extraire_clauses_depuis_tableaux,
)
from dgssi_platform.infrastructure.extraction.regex.extracteur_constats_tableaux import (
    extraire_non_conformites_depuis_tableaux,
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
from dgssi_platform.infrastructure.extraction.llm.extracteur_scores_conformite import (
    extraire_scores_conformite,
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
from dgssi_platform.infrastructure.extraction.llm.extracteur_perimetre import extraire_perimetre_llm
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
        historique = _convertir_versions(historique_brut)
        resultats_element, conf_resultats = extraire_resultats_par_element(tableaux)

        # --- LLM-first : scores de conformité et prestataire ---
        # Le LLM absorbe les variations de notation entre prestataires
        # (pourcentage, /5, lettre, répartition, graphe avec légende...)
        scores_llm, conf_scores = extraire_scores_conformite(texte, tableaux)
        taux_global = scores_llm.get("taux_conformite_global")
        prestataire = scores_llm.get("prestataire")
        systeme_notation = scores_llm.get("systeme_notation", "inconnu")
        valeur_brute = scores_llm.get("valeur_brute", "")
        repartition_llm = scores_llm.get("repartition")
        taux_par_chapitre_llm = scores_llm.get("taux_par_chapitre")
        conf_taux = conf_scores
        conf_prestataire = conf_scores

        # Fallback regex si le LLM n'a trouvé ni taux ni prestataire
        if taux_global is None:
            taux_global, conf_taux = extraire_taux_conformite_global(tableaux)
            if taux_global is not None:
                systeme_notation = "pourcentage"
                valeur_brute = f"{taux_global}%"
        if not prestataire:
            prestataire, conf_prestataire = extraire_prestataire(texte)

        # Les codes DNSSI (...) sont associés aux chapitres par ordre
        # d'apparition (voir extracteur_clauses.py) : les titres Markdown
        # générés par Docling ne sont pas fiables (ex. §3.4 "Gestion des
        # actifs informationnels" n'est pas détectée comme titre).
        noms_chapitres = obtenir_noms_chapitres_ordonnes()
        clauses_par_chapitre, conf_clauses = extraire_clauses_par_chapitre(texte, noms_chapitres)

        # Fallback tableaux : si le texte ne contient pas les codes DNSSI
        # (cas typique des rapports DOCX organisationnels où tout est dans les cellules)
        if conf_clauses < 0.3:
            logger.info(
                "Clauses texte insuffisantes (conf=%.2f) — fallback extracteur tableaux",
                conf_clauses,
            )
            clauses_par_chapitre_tab, conf_clauses_tab = extraire_clauses_depuis_tableaux(
                tableaux, noms_chapitres
            )
            if conf_clauses_tab > conf_clauses:
                clauses_par_chapitre = clauses_par_chapitre_tab
                conf_clauses = conf_clauses_tab
                logger.info("Fallback tableaux adopte (conf=%.2f)", conf_clauses)

        non_conformites, conf_llm = extraire_non_conformites(texte, clauses_par_chapitre, tableaux)

        # Fallback tableaux pour les constats : si le LLM n'a rien trouvé
        # (pas de pattern '- -' dans le texte, constats dans les cellules)
        if not non_conformites and clauses_par_chapitre:
            logger.info("Constats LLM=0 — fallback extracteur constats tableaux")
            non_conformites_tab, conf_nc_tab = extraire_non_conformites_depuis_tableaux(tableaux)
            if non_conformites_tab:
                non_conformites = non_conformites_tab
                conf_llm = conf_nc_tab
                logger.info(
                    "Fallback constats tableaux adopte : %d non-conformites",
                    len(non_conformites),
                )

        # Regroupement par chapitre — permet de peupler ChapitreAudit.constats
        # en plus de la liste à plat Audit.non_conformites. Les deux
        # contiennent les mêmes objets (traçabilité + lecture par chapitre
        # pour le reporting), ce n'est pas une duplication de données, juste
        # deux vues sur la même source.
        non_conformites_par_chapitre: dict[str, list] = {}
        for nc in non_conformites:
            non_conformites_par_chapitre.setdefault(nc.chapitre, []).append(nc)

        # Extraction LLM des périmètres et référentiels (dynamique)
        perimetres, referentiels_llm, conf_llm = extraire_perimetre_llm(texte)

        # Extraction regex des métadonnées techniques (fallbacks et détails)
        referentiels_utilises, conf_ref = extraire_referentiels_utilises(texte)
        if referentiels_llm and conf_llm >= conf_ref:
            referentiels_utilises = referentiels_llm
            conf_ref = conf_llm
        vulnerabilites, conf_vuln = extraire_vulnerabilites_par_categorie(texte)
        audit_technique = (
            AuditTechnique(
                resultats_par_element=resultats_element,
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
                # Cas 1 : notes d'audit explicites dans le texte → synthétiser
                synthese, conf_llm_notes = synthetiser_notes_chapitre(nom, texte_brut)
                conf_notes_list.append(conf_llm_notes)
            elif nom in non_conformites_par_chapitre and non_conformites_par_chapitre[nom]:
                # Cas 2 (Phase 3) : pas de section "Notes d'audit" mais des constats
                # existent → synthétiser les constats pour produire une note
                constats_texte = "\n".join(
                    f"- {nc.resume_constat}" for nc in non_conformites_par_chapitre[nom]
                )
                synthese, conf_llm_notes = synthetiser_notes_chapitre(nom, constats_texte, est_constats=True)
                conf_notes_list.append(conf_llm_notes)
                logger.info(
                    "Synthèse générée depuis constats pour '%s' (%d constats)",
                    nom, len(non_conformites_par_chapitre[nom]),
                )

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
            repartition_globale_controles=repartition_llm or {},
            taux_par_chapitre={
                ch: (t, t) for ch, t in (taux_par_chapitre_llm or {}).items()
            },
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
                "scores_llm": conf_scores,
            },
            nb_ecarts_par_type=totaux_ecarts,
            perimetres=perimetres,
            systeme_notation_source=systeme_notation,
            valeur_brute_source=valeur_brute,
        )