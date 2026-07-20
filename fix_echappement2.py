path = "src/dgssi_platform/infrastructure/extraction/llm/extracteur_constats.py"
with open(path, encoding="utf-8") as f:
    contenu = f.read()

debut_marqueur = "def _nettoyer_echappements_markdown"
fin_marqueur = "def _valider_item_llm"

idx_debut = contenu.find(debut_marqueur)
idx_fin = contenu.find(fin_marqueur)

if idx_debut == -1 or idx_fin == -1:
    print("ERREUR : marqueurs introuvables", idx_debut, idx_fin)
else:
    nouveau_bloc = (
        "def _nettoyer_echappements_markdown(texte: str) -> str:\n"
        '    """Retire les echappements Markdown ajoutes par Docling devant\n'
        "    certains caracteres dans les noms de fichiers cites en texte.\n"
        "    Necessaire car le LLM recopie ces echappements tels quels en\n"
        "    citant le texte source, ce qui produit une sequence non valide\n"
        "    en JSON et fait crasher le parsing (bug identifie sur le\n"
        '    chapitre Conformite)."""\n'
        "    backslash = chr(92)\n"
        '    caracteres_a_nettoyer = "_*[]()#+.-"\n'
        "    for caractere in caracteres_a_nettoyer:\n"
        "        texte = texte.replace(backslash + caractere, caractere)\n"
        "    return texte\n"
        "\n\n"
        "def _extraire_lignes_constats(bloc: str) -> list[str]:\n"
        '    idx = bloc.find("Constats")\n'
        "    if idx == -1:\n"
        "        return []\n"
        '    section = bloc[idx + len("Constats"):].strip(" :' + chr(92) + 'n")[:1500]\n'
        '    lignes = [l.strip() for l in section.split("' + chr(92) + 'n") if l.strip().startswith("-")]\n'
        "    return [_nettoyer_echappements_markdown(l) for l in lignes]\n"
        "\n\n"
    )
    contenu = contenu[:idx_debut] + nouveau_bloc + contenu[idx_fin:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenu)
    print("OK — fonction remplacee proprement")
