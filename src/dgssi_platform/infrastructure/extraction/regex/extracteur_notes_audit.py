"""Extracteur Regex pour isoler la section 'Notes d'audit' par chapitre."""

from __future__ import annotations
import re

from dgssi_platform.infrastructure.extraction.regex.decoupage_chapitres import trouver_ancres_chapitres

def _decouper_blocs_par_chapitre(texte: str, noms_chapitres: list[str]) -> dict[str, str]:
    positions = [m.start() for m in trouver_ancres_chapitres(texte)]
    blocs: dict[str, str] = {}
    for i, nom_chapitre in enumerate(noms_chapitres):
        if i >= len(positions):
            break
        debut = positions[i]
        fin = positions[i + 1] if i + 1 < len(positions) else len(texte)
        blocs[nom_chapitre] = texte[debut:fin]
    return blocs

def extraire_notes_audit_par_chapitre(texte: str, noms_chapitres: list[str]) -> dict[str, tuple[str, float]]:
    """Extrait le texte brut de la section 'Notes d'audit' pour chaque chapitre.
    Retourne un dictionnaire: {nom_chapitre: (texte_brut, confiance)}
    """
    blocs = _decouper_blocs_par_chapitre(texte, noms_chapitres)
    resultats = {}

    for chapitre in noms_chapitres:
        bloc = blocs.get(chapitre, "")
        
        # Recherche du marqueur (insensible à la casse)
        # Certains titres sont "## Notes d'audit : Analyse de risque :"
        match = re.search(r"(?i)notes d'audit\s*[^:\n]*:", bloc)
        if not match:
            # Essayer juste "Notes d'audit" au cas où
            match = re.search(r"(?i)notes d'audit", bloc)
            if not match:
                resultats[chapitre] = ("", 0.0)
                continue
            
        debut_notes = match.end()
        
        # Trouver la fin de la section (soit Preuves, soit Constats, ou autre section principale)
        fin_notes = len(bloc)
        match_preuves = re.search(r"(?im)^#*\s*(?:Preuves|Constats)\s*:?", bloc[debut_notes:])
        
        if match_preuves:
            fin_notes = debut_notes + match_preuves.start()
            
        texte_brut = bloc[debut_notes:fin_notes].strip()
        
        if texte_brut:
            resultats[chapitre] = (texte_brut, 1.0)
        else:
            resultats[chapitre] = ("", 0.0)

    return resultats
