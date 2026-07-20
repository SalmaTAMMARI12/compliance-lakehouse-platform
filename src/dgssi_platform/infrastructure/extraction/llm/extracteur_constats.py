"""Extraction enrichie des non-conformités depuis le texte libre des
constats, via LLM local. Le LLM ne fait QUE de l'enrichissement
documentaire (résumé, recommandation, actifs, échéance) — jamais de
classification ni de décision de conformité (voir non_conformite.py).

Isolation stricte : un échec LLM sur un chapitre ne bloque jamais les
autres chapitres ni le reste du pipeline (retour vide + confiance basse,
jamais d'exception qui remonte) — le LLM est un enrichissement optionnel,
pas une dépendance bloquante du pipeline.
"""

from __future__ import annotations

import re

from dgssi_platform.domain.entities.non_conformite import NonConformite
from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_constats import (
    SYSTEM_PROMPT_CONSTATS,
    construire_user_prompt,
)
from dgssi_platform.infrastructure.extraction.regex.coherence_chapitre import est_coherent_avec_chapitre
from dgssi_platform.infrastructure.extraction.regex.decoupage_chapitres import trouver_ancres_chapitres
from dgssi_platform.shared.logging import get_logger

logger = get_logger(__name__)

VALEURS_RECOMMANDATION_INVALIDES = {"N/A", "NA", "", "AUCUNE", "AUCUN"}


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


def _nettoyer_echappements_markdown(texte: str) -> str:
    """Retire les echappements Markdown ajoutes par Docling devant
    certains caracteres dans les noms de fichiers cites en texte.
    Necessaire car le LLM recopie ces echappements tels quels en
    citant le texte source, ce qui produit une sequence non valide
    en JSON et fait crasher le parsing (bug identifie sur le
    chapitre Conformite)."""
    backslash = chr(92)
    caracteres_a_nettoyer = "_*[]()#+.-"
    for caractere in caracteres_a_nettoyer:
        texte = texte.replace(backslash + caractere, caractere)
    return texte


def _extraire_lignes_constats(bloc: str) -> list[str]:
    idx = bloc.find("Constats")
    if idx == -1:
        return []
    section = bloc[idx + len("Constats"):].strip(" :\n")[:1500]
    lignes = [l.strip() for l in section.split("\n") if l.strip().startswith("-")]
    return [_nettoyer_echappements_markdown(l) for l in lignes]


def _valider_item_llm(item: dict) -> tuple[bool, str]:
    if not isinstance(item, dict):
        return False, "n'est pas un objet"
    resume = item.get("resume_constat", "")
    if not isinstance(resume, str) or len(resume.strip()) < 5:
        return False, "resume_constat vide ou trop court"
    recommandation = item.get("recommandation")
    if recommandation is not None and str(recommandation).strip().upper() in VALEURS_RECOMMANDATION_INVALIDES:
        return False, f"recommandation invalide: {recommandation!r}"
    return True, "ok"


def extraire_non_conformites(
    texte: str, chapitres_avec_codes: dict[str, list[str]]
) -> tuple[list[NonConformite], float]:
    """Pour chaque chapitre, enrichit les constats via LLM. Ne produit
    jamais de classification/décision — voir contrat NonConformite.
    """
    noms_chapitres = list(chapitres_avec_codes.keys())
    blocs = _decouper_blocs_par_chapitre(texte, noms_chapitres)

    toutes_non_conformites: list[NonConformite] = []
    scores: list[float] = []
    nb_a_verifier = 0

    for nom_chapitre, codes in chapitres_avec_codes.items():
        bloc = blocs.get(nom_chapitre, "")
        lignes_constats = _extraire_lignes_constats(bloc)

        if not lignes_constats or "aucun écart" in bloc.lower():
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
            resume = item["resume_constat"]
            coherent = est_coherent_avec_chapitre(resume, codes)
            if not coherent:
                nb_a_verifier += 1

            toutes_non_conformites.append(
                NonConformite(
                    chapitre=nom_chapitre,
                    texte_source=texte_source,
                    resume_constat=resume,
                    recommandation=item.get("recommandation"),
                    actifs_concernes=item.get("actifs_concernes") or [],
                    echeance=item.get("echeance"),
                    confiance=confiance,
                    methode_extraction="llm",
                    a_verifier=not coherent,
                )
            )

    confiance_moyenne = sum(scores) / len(scores) if scores else 0.0
    if nb_a_verifier:
        logger.warning(
            "%d/%d non-conformités marquées a_verifier (incohérence chapitre détectée)",
            nb_a_verifier, len(toutes_non_conformites),
        )
    return toutes_non_conformites, confiance_moyenne
