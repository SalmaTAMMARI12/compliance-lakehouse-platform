from pathlib import Path
from dgssi_platform.infrastructure.extraction.llm.extracteur_constats import (
    _decouper_blocs_par_chapitre,
    _extraire_lignes_constats,
)
from dgssi_platform.infrastructure.extraction.regex.decoupage_chapitres import trouver_ancres_chapitres

texte = Path("texte_complet_rapport.md").read_text(encoding="utf-8")
noms_chapitres = [
    "Politique de sécurité des systèmes d'information",
    "Organisation de la sécurité des systèmes d'information",
    "Sécurité des ressources humaines",
    "Gestion des actifs informationnels",
    "Contrôle d'accès",
    "Cryptographie",
    "Sécurité physique",
    "Sécurité liée à l'exploitation",
    "Sécurité des communications",
    "Acquisition, développement et maintenance des systèmes d'information",
    "Relations avec les fournisseurs",
    "Gestion des incidents de cybersécurité",
    "Gestion du plan de continuité de l'activité",
    "Conformité",
]

blocs = _decouper_blocs_par_chapitre(texte, noms_chapitres)
lignes = _extraire_lignes_constats(blocs["Conformité"])

print("=== Constats NETTOYÉS (après correction) ===")
for l in lignes:
    print(repr(l))
