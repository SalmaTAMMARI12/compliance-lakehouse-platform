"""Entité Audit — une mission d'audit DNSSI, un document PASSI.

Chaque champ est traçable à une page précise du rapport de référence
(voir commentaires). Rien n'est ajouté "pour plus tard" sans preuve.
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

from dgssi_platform.domain.entities.iiv import IIV
from dgssi_platform.domain.entities.non_conformite import NonConformite


class VersionDocument(BaseModel):
    """Une ligne du tableau "Historique des mises à jour" (page 2)."""

    version: str        # "V1.0", "V1.1", "V1.2"
    date: date
    commentaire: str    # "Version initiale", "Modifiée et partagée avec l'audité"...
class ChapitreAudit(BaseModel):
    """Un des 14 blocs répétés en §3.1 à §3.14 — structure vérifiée identique
    sur les 14 occurrences du rapport.
    """

    nom_chapitre: str
    clauses: list[str] = []
    # Codes du référentiel DNSSI (ex. "POL-RISQUE"). Le libellé/objectif de
    # chaque clause vit dans infrastructure/referentiel/, pas ici — on ne
    # référence que le code.

    objectifs: str
    points_de_controle: list[str] = []
    # notes_audit: str
    notes_audit_synthese: str | None = None
    preuves: list[str] = []
    constats: list[str] = []
    # Texte libre — parfois une seule phrase "Conforme aux exigences. Aucun
    # écart relevé." (vérifié §3.2, §3.3, §3.7). PAS encore structuré en
    # NonConformite ici : ça sera une extraction ultérieure (NLP/LLM).


class AuditTechnique(BaseModel):
    """§4 du rapport — échelle de sévérité et structure différentes de la
    conformité DNSSI (organisé par équipement, pas par chapitre).
    """

    referentiels_utilises: list[str] = []         # §4.3 : CIS Benchmarks, DISA STIGs...
    nb_controles_verifies: int | None = None      # §2.1 : "199 contrôles vérifiés"
    nb_constats_majeurs: int | None = None        # §2.1 : "18 majeurs"

    resultats_par_element: dict[str, dict[str, int]] = {}
    # §4.5.a : ex. {"Serveur web Alpha": {"CRITIQUE": 6, "ELEVEE": 14, ...}}
    # La donnée la plus fiable de toute cette section — un vrai tableau chiffré.

    points_amelioration_architecture: list[str] = []
    # §4.5.c : 4 points nommés (protection accès réseau, réseau admin, etc.)

    points_amelioration_par_categorie: dict[str, list[str]] = {}
    # §4.5.d : le document structure lui-même en 3 catégories nommées
    # ("équipements de sécurité et du réseau", "serveur de messagerie",
    # "serveur web") — on respecte cette structure plutôt que de l'aplatir.
class Audit(BaseModel):
    """Une mission d'audit DNSSI — un document PASSI. Chaque champ tracé à
    une page précise du rapport de référence.
    """

    iiv: IIV
    classification: str                              # page 2
    historique_versions: list[VersionDocument] = []  # page 2
    prestataire_audit: str                            # page 4
    cadre_reglementaire: list[str] = []                # page 4
    perimetres: dict[str, list[str]] = {}              # Dictionnaire dynamique des périmètres (ex: Fonctionnel, Technique, etc.)

    taux_conformite_global: float | None = None        # page 9 : 76,70%
    repartition_globale_controles: dict[str, float] = {}
    # page 9 (Figure 1) : {"Non_Conforme": 7.84, "Partielle": 15.69, "Totale": 76.47}

    taux_par_chapitre: dict[str, tuple[float, float]] = {}
    # page 10 : {"Cryptographie": (50.0, 100.0), ...} — (conformité totale %, partielle+totale %)

    nb_ecarts_par_type: dict[str, int] = {}
    # page 10-11 : {"significatif": 11, "non_significatif": 7, "remarque": 1}

    chapitres: list[ChapitreAudit] = []               # pages 12-34
    non_conformites: list[NonConformite] = []          # extraction LLM (constats en texte libre)
    audit_technique: AuditTechnique | None = None      # pages 35-40

    confiance_extraction: dict[str, float] = {}
    # Confiance par catégorie de champ, ex. {"classif": 1.0, "historique": 0.9,
    # "taux": 1.0, "resultats": 1.0, "prestataire": 0.9, "clauses": 1.0, "llm": 0.7}
    # Persiste ce qui aujourd'hui n'existe que dans les logs — traçabilité de
    # fiabilité par champ, exigée par la gouvernance des données de la fiche de
    # stage. Pas de "methode_extraction" par champ ici : tous les champs de
    # Audit sont en Regex sauf non_conformites (déjà tracé sur NonConformite
    # elle-même) — un champ répété partout avec la même valeur "regex" ne
    # serait pas une vraie information.

    # Traçabilité du système de notation du prestataire — chaque prestataire
    # d'audit utilise sa propre notation (pourcentage, /5, lettre, répartition).
    # Le taux_conformite_global est toujours normalisé en %, mais ces champs
    # gardent la trace de la valeur et du système originaux pour la gouvernance.
    systeme_notation_source: str = "pourcentage"
    # "pourcentage" | "note_sur_5" | "note_sur_10" | "lettre" | "repartition" | "inconnu"
    valeur_brute_source: str = ""
    # La valeur telle qu'écrite dans le rapport, ex. "76,70%", "3.2/5", "B+"

