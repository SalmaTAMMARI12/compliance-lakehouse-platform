# AuditDataPlatform — Plateforme Data d'Audit Automatisé

> **Projet de Fin d'Études** · DGSSI · Division Contrôle et Expertise  
> Automatisation du traitement des rapports d'audit de conformité des Infrastructures d'Importance Vitale (IIV) au référentiel national **DNSSI v2**.

---

## Aperçu

**AuditDataPlatform** est une plateforme de données complète qui transforme des rapports d'audit bruts (PDF, DOCX) en indicateurs de conformité exploitables, sans intervention humaine systématique. Elle s'appuie sur un pipeline **ELT** combinant un **Data Lake objet** (MinIO — zones Bronze/Silver/Gold) pour le stockage et la traçabilité, et un **Data Warehouse analytique** (PostgreSQL + dbt) pour la modélisation et le reporting.


---

## Tableau de Bord

> *(Insérez ici votre capture d'écran : `![Dashboard](logos/dash-overview.png)`)*

---

## Architecture Technique

```
                  ┌──────────────────────────────────────┐
                  │       DÉPÔT (data/private/)           │
                  │  Utilisateur dépose PDF ou DOCX       │
                  └──────────────────┬───────────────────┘
                                     │ Surveillance automatique
                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              APACHE NIFI 1.27 — Couche d'Ingestion              │
│  · Détection automatique du nouveau fichier dans le répertoire  │
│  · Validation et routage selon le format (PDF / DOCX)          │
│  · Attribution UUID + horodatage + métadonnées de contexte     │
│  · Upload sécurisé vers MinIO (zone Bronze)                    │
│  Flow configuré et exporté : docker/nifi/flow_export.json      │
└────────────────────────┬────────────────────────────────────────┘
                         │ Upload automatique
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ZONE BRONZE (MinIO)                         │
│           Fichiers bruts · PDF · DOCX · Originaux              │
│                   Conservation intégrale des sources            │
└────────────────────────┬────────────────────────────────────────┘
                         │ Parsing
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ZONE SILVER (MinIO)                         │
│         Texte structuré Markdown · Tableaux extraits           │
│      PDF → Docling    |    DOCX → python-docx (10x plus vite) │
└────────────────────────┬────────────────────────────────────────┘
                         │ Extraction Hybride
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ZONE GOLD (MinIO + PostgreSQL)             │
│   LLM Qwen 2.5 (llama-cpp) : scores, constats, périmètres     │
│   Regex (fallback)          : clauses DNSSI, métadonnées       │
│   Score de confiance par champ extrait                         │
└────────────────────────┬────────────────────────────────────────┘
                         │ dbt (schéma en étoile)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA WAREHOUSE (PostgreSQL)                   │
│  dim_iiv · dim_audit · dim_chapitre_dnssi                      │
│  fact_conformite · fact_non_conformite                         │
│  fact_chapitre_audit · fact_resultats_techniques               │
│  65 tests de qualité automatiques (dbt)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │ Flask
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TABLEAU DE BORD (Flask)                         │
│  Vue Générale · Volet Organisationnel · Volet Technique        │
│  Traçabilité LLM · Historique des versions                     │
│  Masquage dynamique selon le type d'audit                      │
└─────────────────────────────────────────────────────────────────┘
```

**Orchestration** : Apache Airflow (1 DAG, 6 étapes)  
**Supervision** : Prometheus + Grafana (métriques PostgreSQL + conteneurs)  
**Conteneurisation** : Docker Compose (9 services)

---

## Structure du Projet

```
compliance-lakehouse-platform/
│
├── src/dgssi_platform/               # Code source principal
│   ├── domain/                       # Cœur métier (sans dépendances externes)
│   │   ├── entities/                 # Entités : Audit, IIV, NonConformite, Exigence
│   │   └── interfaces/               # Contrats : Parseur, Extracteur
│   │
│   ├── infrastructure/               # Implémentations techniques
│   │   ├── parsing/
│   │   │   ├── docling/              # Parseur PDF (Docling)
│   │   │   └── office/               # Parseur DOCX (python-docx, 10x plus rapide)
│   │   ├── extraction/
│   │   │   ├── extracteur_hybride.py # Chef d'orchestre LLM + Regex
│   │   │   ├── llm/                  # 7 extracteurs LLM (scores, constats, périmètre...)
│   │   │   └── regex/                # 14 extracteurs Regex (clauses, métadonnées, chiffres...)
│   │   ├── database/
│   │   │   ├── models/               # Modèles SQLAlchemy (ORM)
│   │   │   ├── repositories/         # Sauvegarde Audit + Évaluations
│   │   │   └── session.py            # Connexion PostgreSQL
│   │   ├── storage/                  # Client MinIO (zones Bronze/Silver/Gold)
│   │   └── referentiel/              # Loader du référentiel DNSSI v2 (104 exigences)
│   │
│   └── shared/                       # Config et Logging centralisés
│
├── scripts/                          # Scripts d'exécution du pipeline
│   ├── executer_pipeline_complet.py  # Pipeline de bout en bout
│   ├── extraire_audit_depuis_silver.py
│   ├── etl_vers_warehouse.py
│   └── comparer_parseurs.py          # Benchmark Docling vs python-docx
│
├── dbt_project/                      # Transformations et modèles dbt
│   ├── models/staging/               # 6 modèles de staging (nettoyage)
│   ├── models/marts/                 # 7 modèles (3 dimensions + 4 faits)
│   └── seeds/                        # Référentiel DNSSI v2 (chapitres fixes)
│
├── airflow/dags/                     # Orchestration (1 DAG, 6 tâches)
├── docker/                           # Config Docker sur-mesure
│   ├── airflow/Dockerfile            # Airflow + dbt + Docker CLI
│   ├── worker/Dockerfile             # Worker isolé (Docling + SQLAlchemy 2.x)
│   ├── grafana/provisioning/         # Dashboard Grafana auto-provisionné
│   └── prometheus/prometheus.yml     # Scraping PostgreSQL + cAdvisor
├── docker-compose.yaml               # 9 services orchestrés
├── dashboard.py                      # Application web Flask
└── tests/                            # Tests unitaires et d'intégration
```

---

## Stack Technologique

| Couche | Technologies |
|---|---|
| **Ingestion** | Apache NiFi 1.27 |
| **Stockage objet** | MinIO (compatible S3) |
| **Parsing documentaire** | Docling (PDF) · python-docx (DOCX) |
| **Intelligence Artificielle** | Qwen 2.5 via llama-cpp-python (local, sans GPU) |
| **Extraction déterministe** | Expressions régulières (14 extracteurs spécialisés) |
| **Entrepôt de données** | PostgreSQL 16 + dbt-core 1.8 |
| **Schéma analytique** | Schéma en étoile (3 dimensions, 4 faits) |
| **Qualité des données** | 65 tests dbt automatiques |
| **Tableau de bord** | Flask (Python) |
| **Supervision** | Prometheus + Grafana + cAdvisor |
| **Orchestration** | Apache Airflow 2.10 |
| **Conteneurisation** | Docker Compose (9 services) |

---

## Lancement

```bash
# 1. Configurer l'environnement
cp .env.example .env
# Renseigner LLM_MODEL_PATH vers votre fichier .gguf

# 2. Démarrer l'infrastructure
docker compose up -d

# 3. Exécuter le pipeline sur un rapport
python scripts/executer_pipeline_complet.py --rapport data/private/rapport.pdf

# 4. Lancer le tableau de bord
python dashboard.py
# → http://localhost:5000

# 5. Accès aux services
# Airflow   → http://localhost:8085
# Grafana   → http://localhost:3000
# MinIO     → http://localhost:9001
```

---

## Chiffres Clés

| Indicateur | Valeur |
|---|---|
| Exigences DNSSI v2 couvertes | **104 / 104** (100%) |
| Tests de qualité dbt | **65 tests** automatiques |
| Extracteurs Regex spécialisés | **14 extracteurs** |
| Extracteurs LLM spécialisés | **7 extracteurs** |
| Score de confiance (données structurées) | **> 0.75** |
| Formats d'entrée supportés | PDF · DOCX |
| Services Docker | **9 conteneurs** |

---

## Auteur

**Salma TAMMARI**  
Projet de Fin d'Études — ENSIAS  
Stage effectué à la **Direction Générale de la Sécurité des Systèmes d'Information (DGSSI)**  
Division Contrôle et Expertise · Lt. Colonel Mohammed EL MAATAOUI  
Encadrant : M. Youssef IBNOUMALIK
