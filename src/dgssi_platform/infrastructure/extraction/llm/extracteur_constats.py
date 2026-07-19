"""Extraction des non-conformités depuis le texte libre des constats, via
LLM local pour description/recommandation, et classification par règles
Python pour le type (voir classification_ecarts.py).

Isolation stricte : un échec LLM sur un chapitre ne bloque jamais les
autres chapitres ni le reste du pipeline (retour vide + confiance basse,
jamais d'exception qui remonte).
"""

from __future__ import annotations

from dgssi_platform.domain.entities.non_conformite import NonConformite
from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_constats import (
    SYSTEM_PROMPT_CONSTATS,
    construire_user_prompt,
)
from dgssi_platform.infrastructure.extraction.regex.classification_ecarts import classifier_type_ecart
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


def _extraire_lignes_constats(bloc: str) -> list[str]:
    """Isole les lignes de constats (commençant par '-') après le mot
    'Constats' dans un bloc de chapitre."""
    idx = bloc.find("Constats")
    if idx == -1:
        return []
    section = bloc[idx + len("Constats"):].strip(" :\n")[:1500]
    return [l.strip() for l in section.split("\n") if l.strip().startswith("-")]


def _valider_item_llm(item: dict) -> tuple[bool, str]:
    if not isinstance(item, dict):
        return False, "n'est pas un objet"
    description = item.get("description", "")
    if not isinstance(description, str) or len(description.strip()) < 5:
        return False, "description vide ou trop courte"
    recommandation = item.get("recommandation")
    if recommandation is not None and str(recommandation).strip().upper() in VALEURS_RECOMMANDATION_INVALIDES:
        return False, f"recommandation invalide: {recommandation!r}"
    return True, "ok"


def extraire_non_conformites(
    texte: str, chapitres_avec_codes: dict[str, list[str]]
) -> tuple[list[NonConformite], float]:
    """Pour chaque chapitre, extrait les non-conformités : description et
    recommandation via LLM, type via classification Python. Retourne la
    liste complète + une confiance moyenne sur l'ensemble.
    """
    noms_chapitres = list(chapitres_avec_codes.keys())
    blocs = _decouper_blocs_par_chapitre(texte, noms_chapitres)

    toutes_non_conformites: list[NonConformite] = []
    scores: list[float] = []

    for nom_chapitre, codes in chapitres_avec_codes.items():
        bloc = blocs.get(nom_chapitre, "")
        lignes_constats = _extraire_lignes_constats(bloc)

        if not lignes_constats or "aucun écart" in bloc.lower():
            scores.append(1.0)  # rien à extraire, cas normal et fiable
            continue

        texte_constats = "\n".join(lignes_constats)
        user_prompt = construire_user_prompt(
            nom_chapitre=nom_chapitre,
            codes_dnssi=", ".join(codes),
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
            toutes_non_conformites.append(
                NonConformite(
                    chapitre=nom_chapitre,
                    type=classifier_type_ecart(texte_source),
                    description=item["description"],
                    recommandation=item.get("recommandation"),
                )
            )

    confiance_moyenne = sum(scores) / len(scores) if scores else 0.0
    return toutes_non_conformites, confiance_moyenne
