"""Extraction des codes de clauses DNSSI depuis les TABLEAUX du rapport.

Utilisé en fallback lorsque l'extracteur texte ne trouve rien — cas typique
des rapports DOCX d'audit organisationnel où le contenu est dans les cellules
plutôt que dans le texte markdown.

Format attendu dans les tables :
  - "POL-RISQUE : Analyse de risque"
  - "DNSSI- POL-FORMEL : Politique de sécurité des SI"
  - "ORG-STRUCT : Structure organisationnelle"
  - "ACTIF-RESP-INV : Inventaire des actifs"  (préfixe long, même chapitre que ACT)

Mapping domaine → chapitre DNSSI (ordre officiel DNSSI v2) :
  POL / — → Politique de sécurité des systèmes d'information
  ORG / — → Organisation de la sécurité
  RH  / — → Sécurité des ressources humaines
  ACT / ACTIF → Gestion des actifs informationnels
  ACC / — → Contrôle d'accès
  CRYPT / CRYPTO → Cryptographie
  PHYS / — → Sécurité physique
  EXP / — → Sécurité liée à l'exploitation
  COM / — → Sécurité des communications
  DEV / — → Acquisition, développement et maintenance des SI
  FOU / FOURNIS → Relations avec les fournisseurs
  INC / INCID → Gestion des incidents de cybersécurité
  PCA / CONTINU → Gestion de la continuité de l'activité
  CONF / — → Conformité
"""
from __future__ import annotations

import re

from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

# Pattern : "DNSSI- POL-RISQUE : ..." ou "POL-RISQUE : ..." ou "ACC-UTILIS : ..."
# Accepte 2 à 8 lettres pour le préfixe (FOURNIS = 7, CONTINU = 7)
_PATTERN_CODE_CELLULE = re.compile(
    r"^(?:DNSSI[-\s]*)?"             # préfixe DNSSI optionnel
    r"([A-Z]{2,8}(?:-[A-Z0-9/]+)+)" # code ex. POL-RISQUE, ACTIF-RESP-INV, FOURNIS-REL-RISQ
    r"\s*[:\-–]",                    # séparateur
    re.IGNORECASE,
)

# Correspondance préfixe → nom de chapitre (ordre DNSSI v2)
# Inclut les préfixes courts (rapport PDF) ET longs (rapport DOCX / dnssi_v2.yaml)
_PREFIXE_VERS_CHAPITRE: dict[str, str] = {
    # Préfixes courts (rapport PDF de référence)
    "POL":   "Politique de sécurité des systèmes d'information",
    "ORG":   "Organisation de la sécurité des systèmes d'information",
    "RH":    "Sécurité des ressources humaines",
    "ACT":   "Gestion des actifs informationnels",
    "ACC":   "Contrôle d'accès",
    "CRYPT": "Cryptographie",
    "PHYS":  "Sécurité physique et environnementale",
    "EXP":   "Sécurité liée à l'exploitation",
    "COM":   "Sécurité des communications",
    "DEV":   "Acquisition, développement et maintenance des systèmes d'information",
    "FOU":   "Relations avec les fournisseurs",
    "INC":   "Gestion des incidents de cybersécurité",
    "PCA":   "Gestion de la continuité de l'activité",
    "CONF":  "Conformité",
    # Préfixes longs (dnssi_v2.yaml / rapports DOCX de certains prestataires)
    "ACTIF":   "Gestion des actifs informationnels",
    "CRYPTO":  "Cryptographie",
    "FOURNIS": "Relations avec les fournisseurs",
    "INCID":   "Gestion des incidents de cybersécurité",
    "CONTINU": "Gestion de la continuité de l'activité",
}

# Faux positifs — mots français courants avec un tiret qui matchent le pattern
# de code DNSSI (2-8 lettres majuscules + tiret + lettres). Le filtre s'applique
# sur le préfixe (partie avant le premier tiret).
_FAUX_POSITIFS_PREFIXES: set[str] = {
    "PARE",      # PARE-FEU
    "SOUS",      # SOUS-TRAITANTS, SOUS-RÉSEAU
    "SUPER",     # SUPER-UTILISATEUR
    "DEFFIE",    # DEFFIE-HELLMAN (faute courante dans les rapports)
    "DIFFIE",    # DIFFIE-HELLMAN
    "NON",       # NON-CONFORMITÉ, NON-SIGNIFICATIF
    "CELLES",    # CELLES-CI
    "CEUX",      # CEUX-CI
    "CELUI",      # CELUI-CI
    "CELLE",      # CELLE-CI
    "PEUT",      # PEUT-ÊTRE (rare dans cellules mais possible)
    "SEMI",      # SEMI-AUTOMATIQUE
    "ANTI",      # ANTI-VIRUS, ANTI-MALWARE
    "MULTI",     # MULTI-FACTEUR
    "AUTO",      # AUTO-ÉVALUATION
    "POST",      # POST-INCIDENT
    "PRE",       # PRE-AUDIT
}


def _extraire_code(cellule: str) -> str | None:
    """Extrait le code DNSSI d'une cellule de tableau, ou None.
    Filtre les faux positifs (mots français courants avec tiret).
    """
    m = _PATTERN_CODE_CELLULE.match(cellule.strip())
    if not m:
        return None
    code = m.group(1).upper()
    prefixe = code.split("-")[0] if "-" in code else code
    if prefixe in _FAUX_POSITIFS_PREFIXES:
        return None
    return code


def _prefixe_du_code(code: str) -> str | None:
    """Retourne le préfixe (ex. 'POL' pour 'POL-RISQUE', 'ACTIF' pour 'ACTIF-RESP-INV')."""
    return code.split("-")[0] if "-" in code else None


def extraire_clauses_depuis_tableaux(
    tableaux: list[list[list[str]]],
    noms_chapitres_ordonnes: list[str],
) -> tuple[dict[str, list[str]], float]:
    """Parcourt les tableaux et regroupe les codes DNSSI par chapitre.

    Retourne (clauses_par_chapitre, confiance).
    Confiance = nb chapitres couverts / nb chapitres attendus.
    """
    clauses_par_chapitre: dict[str, list[str]] = {}

    for tableau in tableaux:
        for ligne in tableau:
            for cellule in ligne:
                code = _extraire_code(str(cellule))
                if not code:
                    continue
                prefixe = _prefixe_du_code(code)
                if not prefixe:
                    continue
                nom_chapitre = _PREFIXE_VERS_CHAPITRE.get(prefixe)
                if not nom_chapitre:
                    logger.debug("Prefixe inconnu dans code DNSSI : %s", code)
                    continue
                if nom_chapitre not in clauses_par_chapitre:
                    clauses_par_chapitre[nom_chapitre] = []
                if code not in clauses_par_chapitre[nom_chapitre]:
                    clauses_par_chapitre[nom_chapitre].append(code)

    nb_couverts = len(clauses_par_chapitre)
    nb_attendus = len(noms_chapitres_ordonnes) if noms_chapitres_ordonnes else 14
    confiance = nb_couverts / nb_attendus if nb_attendus else 0.0

    logger.info(
        "Clauses depuis tableaux : %d chapitres couverts / %d attendus (confiance=%.2f)",
        nb_couverts, nb_attendus, confiance,
    )
    return clauses_par_chapitre, confiance
