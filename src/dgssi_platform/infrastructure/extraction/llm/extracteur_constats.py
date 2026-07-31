"""Extraction des non-conformités depuis le texte libre des constats, via
LLM local pour description/recommandation, classification par règles
Python pour le type, et vérification de cohérence thématique pour
signaler les cas où Docling a mal associé le texte au bon chapitre.

Supporte deux sources de constats :
1. Texte Markdown (PDF via Docling) — constats au format "- - constat"
2. Tableaux (DOCX via python-docx) — constats dans les cellules "Constat: ..."

Le texte enrichi (texte + tableaux formatés) est construit automatiquement
quand la source texte ne contient pas de constats exploitables — typique
des rapports DOCX organisationnels.

Isolation stricte : un échec LLM sur un chapitre ne bloque jamais les
autres chapitres ni le reste du pipeline (retour vide + confiance basse,
jamais d'exception qui remonte).
"""

from __future__ import annotations

import re

from dgssi_platform.domain.entities.non_conformite import NonConformite
from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_constats import (
    SYSTEM_PROMPT_CONSTATS,
    construire_user_prompt,
)
from dgssi_platform.infrastructure.extraction.llm.texte_enrichi import (
    construire_texte_enrichi,
)
from dgssi_platform.infrastructure.extraction.regex.classification_ecarts import classifier_type_ecart
from dgssi_platform.infrastructure.extraction.regex.coherence_chapitre import est_coherent_avec_chapitre
from dgssi_platform.infrastructure.extraction.regex.decoupage_chapitres import trouver_ancres_chapitres
from dgssi_platform.infrastructure.extraction.regex.filtre_faux_constats import est_probable_faux_constat
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

VALEURS_RECOMMANDATION_INVALIDES = {"N/A", "NA", "", "AUCUNE", "AUCUN"}

# Pattern pour découper le texte enrichi par chapitre (codes DNSSI comme ancres)
_PATTERN_CODE_DNSSI_ANCRE = re.compile(
    r"---\s*\[(?:DNSSI[-\s]*)?([A-Z]{2,8}(?:-[A-Z0-9/]+)+)\s*[:\-–]",
    re.IGNORECASE,
)


def _decouper_blocs_par_chapitre(texte: str, noms_chapitres: list[str]) -> dict[str, str]:
    positions = [m.start() for m in trouver_ancres_chapitres(texte)]
    if len(positions) != len(noms_chapitres):
        logger.warning(
            "%d ancres trouvées pour %d chapitres attendus — découpage potentiellement décalé",
            len(positions), len(noms_chapitres),
        )
    blocs: dict[str, str] = {}
    for i, nom_chapitre in enumerate(noms_chapitres):
        if i >= len(positions):
            break
        debut = positions[i]
        fin = positions[i + 1] if i + 1 < len(positions) else len(texte)
        blocs[nom_chapitre] = texte[debut:fin]
    return blocs


def _decouper_texte_enrichi_par_chapitre(
    texte_enrichi: str,
    chapitres_avec_codes: dict[str, list[str]],
) -> dict[str, str]:
    """Découpe le texte enrichi par chapitre en utilisant les codes DNSSI comme ancres.

    Construit un index inversé code → nom_chapitre, puis cherche les ancres
    "--- [CODE-DNSSI : ...]---" dans le texte enrichi pour délimiter les blocs.
    Les codes d'un même chapitre sont regroupés dans un seul bloc.
    """
    from dgssi_platform.infrastructure.extraction.regex.extracteur_clauses_tableaux import (
        _PREFIXE_VERS_CHAPITRE,
    )

    # Index inversé : préfixe de code → nom de chapitre
    # (on utilise le mapping existant pour résoudre le préfixe)
    blocs: dict[str, list[str]] = {nom: [] for nom in chapitres_avec_codes}

    # Chercher toutes les ancres dans le texte enrichi
    matches = list(_PATTERN_CODE_DNSSI_ANCRE.finditer(texte_enrichi))
    if not matches:
        logger.info("Aucune ancre DNSSI trouvée dans le texte enrichi")
        return {}

    for i, match in enumerate(matches):
        code = match.group(1).upper()
        prefixe = code.split("-")[0] if "-" in code else code
        nom_chapitre = _PREFIXE_VERS_CHAPITRE.get(prefixe)

        if not nom_chapitre or nom_chapitre not in chapitres_avec_codes:
            continue

        debut = match.start()
        fin = matches[i + 1].start() if i + 1 < len(matches) else len(texte_enrichi)
        blocs[nom_chapitre].append(texte_enrichi[debut:fin])

    # Fusionner les fragments de chaque chapitre
    return {nom: "\n".join(fragments) for nom, fragments in blocs.items() if fragments}


def _extraire_lignes_constats(bloc: str) -> list[str]:
    lignes = bloc.split("\n")
    constats_inverses = []

    for i in range(len(lignes) - 1, -1, -1):
        ligne = lignes[i].strip()

        if ligne.startswith("- -"):
            constats_inverses.append(ligne)
            for j in range(i - 1, -1, -1):
                ligne_prec = lignes[j].strip()
                if not ligne_prec:
                    continue
                if ligne_prec.startswith("- -"):
                    constats_inverses.append(ligne_prec)
                elif ligne_prec.startswith("- "):
                    break
                else:
                    break
            break

    constats = list(reversed(constats_inverses))

    if not constats:
        idx = bloc.find("Constats")
        if idx != -1:
            section = bloc[idx + len("Constats"):].strip(" :\n")[:1500]
            return [l.strip() for l in section.split("\n") if l.strip().startswith("-")]

    return constats


def _extraire_lignes_constats_enrichi(bloc_enrichi: str) -> list[str]:
    """Extrait les lignes de constats depuis un bloc de texte enrichi (tableaux formatés).

    Dans le texte enrichi, les constats apparaissent sous la forme :
      "Constat : Le dispositif de management des risques..."
    """
    lignes = bloc_enrichi.split("\n")
    constats: list[str] = []

    for ligne in lignes:
        ligne_strip = ligne.strip()
        if not ligne_strip:
            continue
        # Ligne commençant par "Constat :" ou "Constat:"
        if re.match(r"^Constat\s*:", ligne_strip, re.IGNORECASE):
            corps = re.sub(r"^Constat\s*:\s*", "", ligne_strip, flags=re.IGNORECASE).strip()
            if corps and not _est_conforme_texte(corps):
                constats.append(corps)

    return constats


def _est_conforme_texte(texte: str) -> bool:
    """Vérifie si un texte est une simple déclaration de conformité."""
    t = texte.strip().lower()
    return t in {"ras", "conforme", "neant", "n/a", "na"} or t.startswith("conforme")


def _section_declaree_conforme(lignes_constats: list[str]) -> bool:
    """Vérifie si TOUTES les lignes de constats déjà extraites se résument à
    une déclaration de conformité (aucun écart réel) — évalué directement
    sur les lignes qui seraient sinon envoyées au LLM, pas sur une
    recherche du mot "Constats" dans le bloc brut (position peu fiable :
    peut être absente, dupliquée ou déplacée par un artefact de saut de
    page — confirmé sur le chapitre "Organisation", où "Constats"
    n'apparaît qu'une fois, hors contexte, sans lien avec la vraie section
    de fin).
    """
    if not lignes_constats:
        return False
    texte_nettoye = " ".join(
        re.sub(r"^[\s\-–—]+", "", l).strip().lower() for l in lignes_constats
    )
    return texte_nettoye.startswith("conforme")


def _valider_item_llm(item: dict) -> tuple[bool, str]:
    if not isinstance(item, dict):
        return False, "n'est pas un objet"
    description = item.get("resume_constat", "")
    if not isinstance(description, str) or len(description.strip()) < 5:
        return False, "resume_constat vide ou trop court"
    recommandation = item.get("recommandation")
    if recommandation is not None and str(recommandation).strip().upper() in VALEURS_RECOMMANDATION_INVALIDES:
        return False, f"recommandation invalide: {recommandation!r}"
    return True, "ok"


def extraire_non_conformites(
    texte: str,
    chapitres_avec_codes: dict[str, list[str]],
    tableaux: list[list[list[str]]] | None = None,
) -> tuple[list[NonConformite], float]:
    """Pour chaque chapitre, extrait les non-conformités : description et
    recommandation via LLM, type via classification Python, cohérence
    thématique vérifiée pour signaler les cas à revoir manuellement.

    Args:
        texte: Texte Markdown du rapport (Silver).
        chapitres_avec_codes: Dict {nom_chapitre: [codes DNSSI]}.
        tableaux: Tableaux extraits du rapport (Silver). Si fourni, un texte
            enrichi est construit pour les chapitres où le texte ne contient
            pas de constats exploitables.
    """
    noms_chapitres = list(chapitres_avec_codes.keys())
    blocs_texte = _decouper_blocs_par_chapitre(texte, noms_chapitres)

    # Construire le texte enrichi et le découper par chapitre (si tableaux fournis)
    blocs_enrichi: dict[str, str] = {}
    if tableaux:
        texte_enrichi = construire_texte_enrichi(texte, tableaux)
        blocs_enrichi = _decouper_texte_enrichi_par_chapitre(
            texte_enrichi, chapitres_avec_codes
        )
        logger.info(
            "Texte enrichi découpé : %d/%d chapitres avec contenu",
            len(blocs_enrichi), len(noms_chapitres),
        )

    toutes_non_conformites: list[NonConformite] = []
    scores: list[float] = []
    nb_a_verifier = 0

    for nom_chapitre, codes in chapitres_avec_codes.items():
        # --- Stratégie 1 : constats depuis le texte Markdown (PDF) ---
        bloc_texte = blocs_texte.get(nom_chapitre, "")
        lignes_constats = _extraire_lignes_constats(bloc_texte)
        source = "texte"

        # --- Stratégie 2 : si pas de constats texte, essayer le texte enrichi ---
        if not lignes_constats and nom_chapitre in blocs_enrichi:
            lignes_constats = _extraire_lignes_constats_enrichi(
                blocs_enrichi[nom_chapitre]
            )
            source = "tableaux_enrichi"
            if lignes_constats:
                logger.info(
                    "Chapitre '%s' : %d constats trouvés via texte enrichi (tableaux)",
                    nom_chapitre, len(lignes_constats),
                )

        if not lignes_constats:
            scores.append(1.0)
            continue

        if _section_declaree_conforme(lignes_constats):
            scores.append(1.0)
            continue

        texte_constats = "\n".join(lignes_constats)
        user_prompt = construire_user_prompt(
            nom_chapitre=nom_chapitre,
            texte_constats=texte_constats,
            nb_constats=len(lignes_constats),
        )

        resultat, confiance = generer_json_chat(SYSTEM_PROMPT_CONSTATS, user_prompt)
        scores.append(confiance)

        if resultat is None:
            logger.warning("Extraction LLM échouée pour le chapitre %s", nom_chapitre)
            continue

        items_llm = resultat.get("ecarts", [])
        for i, item in enumerate(items_llm):
            ok, raison = _valider_item_llm(item)
            if not ok:
                logger.warning("Item LLM rejeté pour %s : %s -> %s", nom_chapitre, raison, item)
                continue

            texte_source = lignes_constats[i] if i < len(lignes_constats) else ""
            description = item["resume_constat"]

            est_faux = est_probable_faux_constat(texte_source)
            coherent = est_coherent_avec_chapitre(description, codes, texte_source=texte_source)

            a_verifier = est_faux or not coherent
            if a_verifier:
                nb_a_verifier += 1

            toutes_non_conformites.append(
                NonConformite(
                    chapitre=nom_chapitre,
                    texte_source=texte_source,
                    resume_constat=description,
                    recommandation=item.get("recommandation"),
                    actifs_concernes=item.get("actifs_concernes", []),
                    echeance=item.get("echeance"),
                    a_verifier=a_verifier,
                    est_note=False,
                    methode_extraction=f"llm_{source}",
                )
            )

    confiance_moyenne = sum(scores) / len(scores) if scores else 0.0
    if nb_a_verifier:
        logger.warning(
            "%d/%d non-conformités marquées a_verifier (incohérence chapitre détectée)",
            nb_a_verifier, len(toutes_non_conformites),
        )
    return toutes_non_conformites, confiance_moyenne

