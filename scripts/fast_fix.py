import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv()

from dgssi_platform.infrastructure.storage.minio_client import telecharger_objet, telecharger_json, upload_json
from dgssi_platform.infrastructure.extraction.llm.extracteur_perimetre import extraire_perimetre_llm
from dgssi_platform.infrastructure.extraction.regex.extracteur_texte_libre import extraire_prestataire

def fast_fix():
    rapports = ["Exemple de rapport d'audit", "Rapport-Audit-Sécurité-Organisationnelle_DNSSI1"]
    
    for nom_rapport in rapports:
        print(f"\\n--- Traitement de {nom_rapport} ---")
        try:
            texte = telecharger_objet("silver", f"{nom_rapport}/texte.md").decode("utf-8")
            
            print("Extraction des périmètres et référentiels via LLM (patientez ~20s)...")
            perimetres, referentiels, conf = extraire_perimetre_llm(texte)
            print("Nouveaux Périmètres:", perimetres)
            print("Nouveaux Référentiels:", referentiels)

            data = telecharger_json("gold", f"{nom_rapport}.json")
            data["perimetres"] = perimetres
            
            if "audit_technique" not in data or data["audit_technique"] is None:
                data["audit_technique"] = {}
            
            # Pour le PDF, s'il a déjà des réf trouvées par regex, on les garde si le LLM n'en trouve pas
            anciens_ref = data["audit_technique"].get("referentiels_utilises", [])
            if referentiels:
                data["audit_technique"]["referentiels_utilises"] = referentiels
            elif not anciens_ref:
                data["audit_technique"]["referentiels_utilises"] = []
            
            upload_json("gold", f"{nom_rapport}.json", data)
            print("Gold mis à jour avec succès!")
        except Exception as e:
            print(f"Erreur: {e}")

if __name__ == '__main__':
    fast_fix()
