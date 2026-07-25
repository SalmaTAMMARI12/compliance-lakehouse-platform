# DGSSI — Plateforme d'ingénierie et d'analyse des données réglementaires

Plateforme Data Engineering pour l'automatisation de l'analyse documentaire des rapports d'audit de cybersécurité et des dossiers d'homologation des Infrastructures d'Importance Vitale (IIV).

## 1. Prérequis

- **Python** ≥ 3.11
- **Docker Desktop** (pour faire tourner PostgreSQL 16 et MinIO)
- **Git**

## 2. Installation

1. Cloner le dépôt :
   ```bash
   git clone <url_du_depot>
   cd dgssi-compilance
   ```

2. Créer et activer l'environnement virtuel :
   ```bash
   python -m venv venv
   # Sous Windows :
   .\venv\Scripts\activate
   # Sous Linux/Mac :
   source venv/bin/activate
   ```

3. Installer le package et ses dépendances :
   ```bash
   pip install -e ".[database,storage,extraction]"
   ```

4. Configuration :
   Copier le fichier d'exemple et configurer vos chemins si besoin :
   ```bash
   cp .env.example .env
   ```

5. Lancer l'infrastructure (Base de données et Stockage) :
   ```bash
   docker compose up -d
   ```

6. Initialiser la base de données :
   ```bash
   python -c "from dgssi_platform.infrastructure.database.models.audit_model import Base; from sqlalchemy import create_engine; from dgssi_platform.shared.config import get_settings; engine = create_engine(get_settings().postgres_dsn); Base.metadata.create_all(engine)"
   ```

## 3. Modèle LLM

Le projet utilise **llama-cpp-python** pour l'inférence locale sur CPU, sans nécessiter de serveur tiers ni garder le modèle en RAM en permanence.

1. Téléchargez le modèle Qwen 2.5 1.5B Instruct (format GGUF) :  
   [Lien de téléchargement direct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf)

2. Dans votre fichier `.env`, configurez le chemin absolu vers ce fichier :
   ```
   LLM_MODEL_PATH=C:/chemin/vers/qwen2.5-1.5b-instruct-q4_k_m.gguf
   ```

## 4. Lancer une extraction

Pour exécuter le pipeline d'extraction complet (Bronze → Silver → Gold → Postgres) :

```bash
# Pour le pipeline de production complet (inclut le parsing Docling) :
python scripts/extraire_audit_depuis_silver.py <nom_fichier_dans_bronze>

# Pour itérer et tester sans rejouer le parsing lourd de Docling (utilise le Silver existant) :
python scripts/test.py <nom_fichier_dans_bronze>
```

## 5. Dashboard

Pour visualiser les résultats via l'interface web :

```bash
python dashboard.py
```
Le dashboard sera accessible sur [http://127.0.0.1:5000](http://127.0.0.1:5000).

## 6. Limites connues

- **Taux de confiance `a_verifier`** : Le parsing des tableaux PDF s'étalant sur de multiples pages via Docling reste capricieux. Certains constats peuvent être marqués comme "à vérifier" si le moteur détecte une incohérence entre la classe prédite et le chapitre source.
- **Généralisation** : L'extraction par Regex est très performante sur les grilles conformes au modèle de la DGSSI (ex: PASSI). Elle peut nécessiter des ajustements pour des formulations très exotiques d'autres prestataires.
- **Synthèse LLM** : Le modèle Qwen 1.5B est léger pour tourner sur n'importe quelle machine de développement locale. Il peut occasionnellement couper sa réponse en cours de route sur des chapitres très longs (erreur de JSON mal terminé). Le pipeline isole ce problème : le chapitre aura simplement une synthèse nulle sans faire échouer l'audit complet.