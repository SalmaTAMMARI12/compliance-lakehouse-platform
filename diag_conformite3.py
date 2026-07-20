from pathlib import Path
from dgssi_platform.infrastructure.extraction.llm.client_llm import generer_json_chat
from dgssi_platform.infrastructure.extraction.llm.prompts.prompt_constats import (
    SYSTEM_PROMPT_CONSTATS,
    construire_user_prompt,
)
from dgssi_platform.infrastructure.extraction.llm.extracteur_constats import (
    _decouper_blocs_par_chapitre,
    _extraire_lignes_constats,
)

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
texte_constats = "\n".join(lignes)

prompt = construire_user_prompt("Conformité", texte_constats, len(lignes))
resultat, confiance = generer_json_chat(SYSTEM_PROMPT_CONSTATS, prompt, max_tokens=900)

print("Résultat:", "SUCCÈS" if resultat is not None else "ÉCHEC")
print("Confiance:", confiance)
if resultat:
    print("Nombre d'écarts:", len(resultat.get("ecarts", [])))
    for e in resultat["ecarts"][:3]:
        print(" -", e["resume_constat"][:80])
