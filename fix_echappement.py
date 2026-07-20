path = "src/dgssi_platform/infrastructure/extraction/llm/extracteur_constats.py"
with open(path, encoding="utf-8") as f:
    contenu = f.read()

ancien_import = "from __future__ import annotations\n\nfrom dgssi_platform.domain.entities.non_conformite import NonConformite"
nouveau_import = "from __future__ import annotations\n\nimport re\n\nfrom dgssi_platform.domain.entities.non_conformite import NonConformite"

if ancien_import not in contenu:
    print("ERREUR import : anchor introuvable")
else:
    contenu = contenu.replace(ancien_import, nouveau_import, 1)
    print("OK import")

ancien_fn = '''def _extraire_lignes_constats(bloc: str) -> list[str]:
    idx = bloc.find("Constats")
    if idx == -1:
        return []
    section = bloc[idx + len("Constats"):].strip(" :\\n")[:1500]
    return [l.strip() for l in section.split("\\n") if l.strip().startswith("-")]'''

nouveau_fn = '''def _nettoyer_echappements_markdown(texte: str) -> str:
    """Retire les echappements Markdown ajoutes par Docling (ex.
    Securite\\\\_V1\\\\_2023 -> Securite_V1_2023) avant envoi au LLM. Sinon
    le modele les recopie tels quels en citant le texte source, ce qui
    produit un antislash suivi d'un caractere non valide en JSON et fait
    crasher le parsing (cause identifiee du bug sur le chapitre Conformite)."""
    return re.sub(r"\\\\\\\\([_*\\[\\]()#+.-])", r"\\\\1", texte)


def _extraire_lignes_constats(bloc: str) -> list[str]:
    idx = bloc.find("Constats")
    if idx == -1:
        return []
    section = bloc[idx + len("Constats"):].strip(" :\\n")[:1500]
    lignes = [l.strip() for l in section.split("\\n") if l.strip().startswith("-")]
    return [_nettoyer_echappements_markdown(l) for l in lignes]'''

if ancien_fn not in contenu:
    print("ERREUR fonction : anchor introuvable")
else:
    contenu = contenu.replace(ancien_fn, nouveau_fn, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenu)
    print("OK — extracteur_constats.py mis à jour")
