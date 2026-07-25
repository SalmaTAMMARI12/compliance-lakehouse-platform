# 📘 Guide complet — Plateforme de conformité DGSSI / DNSSI v2

> **Auteur** : Salma TAMMARI — Stage ingénieure à la DGSSI  
> **Date** : 21 juillet 2026  
> **Stack** : Windows 11 · Docker · PostgreSQL 16 · MinIO · NiFi · Airflow · dbt · Prometheus · Grafana · Power BI · Flask

---

## Table des matières

1. [Vue d'ensemble de la plateforme](#1--vue-densemble-de-la-plateforme)
2. [Architecture technique](#2--architecture-technique)
3. [Services Docker — Credentials et accès](#3--services-docker--credentials-et-accès)
4. [Ce qui a été fait et pourquoi](#4--ce-qui-a-été-fait-et-pourquoi)
5. [Guide d'utilisation pas à pas](#5--guide-dutilisation-pas-à-pas)
6. [Détail de chaque composant](#6--détail-de-chaque-composant)
7. [Dépannage courant](#7--dépannage-courant)

---

## 1 — Vue d'ensemble de la plateforme

Cette plateforme est un **système de Data Engineering** qui automatise l'analyse de conformité des **IIV** (Infrastructures d'Information Vitales) aux normes **DNSSI v2** (Directive Nationale de la Sécurité des Systèmes d'Information).

### Que fait la plateforme ?

```
📄 Rapport d'audit PDF
   ↓
🔄 NiFi (ingestion automatique)
   ↓
📦 MinIO (stockage Bronze → Silver → Gold)
   ↓
🐍 Python/Docling (extraction intelligente du contenu)
   ↓
🐘 PostgreSQL (base de données relationnelle)
   ↓
🔧 dbt (transformation en schéma étoile pour l'analyse)
   ↓
📊 Power BI + Dashboard Flask (visualisation)
   ↓
🔔 Grafana (monitoring + alertes automatiques)
```

### Pourquoi cette architecture ?

| Couche | Outil | Rôle | Pourquoi ce choix |
|--------|-------|------|-------------------|
| **Ingestion** | NiFi | Récupère les PDF et les dépose dans MinIO | Interface visuelle, traçabilité des flux, gestion des erreurs |
| **Stockage** | MinIO | Stockage objet compatible S3 (Bronze/Silver/Gold) | Architecture Medallion : les données brutes ne sont jamais perdues |
| **Extraction** | Docling + Python | Extrait le texte et les tableaux des PDF | IA pour comprendre la structure des rapports d'audit |
| **Base** | PostgreSQL 16 | Stocke les données structurées | Standard industrie, gratuit, fiable |
| **Transformation** | dbt 1.12 | Transforme les données brutes en modèles analytiques | Tests automatiques, documentation, reproductibilité |
| **Orchestration** | Airflow | Enchaîne les étapes automatiquement | Planification, retry, monitoring des tâches |
| **Visualisation** | Power BI + Flask | Tableaux de bord interactifs | Power BI pour la DGSSI, Flask pour l'accès web |
| **Monitoring** | Prometheus + Grafana | Surveille la santé de PostgreSQL | Alertes automatiques si problème de conformité |

---

## 2 — Architecture technique

```
┌─────────────────────────────────────────────────────────────┐
│                    MACHINE LOCALE (Windows 11)               │
│                         16 GB RAM                            │
│                                                              │
│  ┌──────────────────── Docker Desktop ──────────────────┐   │
│  │                                                       │   │
│  │  ┌─────────┐  ┌─────────┐  ┌──────────┐             │   │
│  │  │ Postgres │  │  MinIO  │  │   NiFi   │             │   │
│  │  │  :5432   │  │:9000/01 │  │  :8443   │             │   │
│  │  └────┬─────┘  └─────────┘  └──────────┘             │   │
│  │       │                                               │   │
│  │  ┌────┴─────┐  ┌───────────────┐                     │   │
│  │  │ Airflow  │  │ PG Exporter   │                     │   │
│  │  │  :8085   │  │    :9187      │                     │   │
│  │  └──────────┘  └───────┬───────┘                     │   │
│  │                        │                              │   │
│  │              ┌─────────┴────────┐                    │   │
│  │              │   Prometheus     │                    │   │
│  │              │     :9090        │                    │   │
│  │              └─────────┬────────┘                    │   │
│  │                        │                              │   │
│  │              ┌─────────┴────────┐                    │   │
│  │              │    Grafana       │                    │   │
│  │              │     :3000        │                    │   │
│  │              └──────────────────┘                    │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──── Venv Python local ────┐  ┌──── Applications ────┐   │
│  │ • Docling (extraction)    │  │ • Power BI Desktop    │   │
│  │ • SQLAlchemy 2.x          │  │ • Dashboard Flask     │   │
│  │ • Scripts Python          │  │   :5000               │   │
│  └───────────────────────────┘  └───────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3 — Services Docker — Credentials et accès

### 🔑 Tableau des accès

| Service | URL | Utilisateur | Mot de passe | Remarques |
|---------|-----|-------------|--------------|-----------|
| **PostgreSQL** | `localhost:5432` | `dgssi` | `changeme` | Base : `dgssi`. Connexion via pgAdmin, DBeaver, ou Power BI |
| **MinIO Console** | http://localhost:9001 | `dgssi_admin` | `changeme123` | Interface web pour gérer les buckets Bronze/Silver/Gold |
| **MinIO API S3** | http://localhost:9000 | `dgssi_admin` | `changeme123` | Utilisé par les scripts Python (`boto3`, `minio`) |
| **Apache NiFi** | https://localhost:8443 | `admin` | `dgssiAdmin123!` | ⚠️ HTTPS avec certificat auto-signé, accepter l'avertissement du navigateur |
| **Airflow** | http://localhost:8085 | `admin` | *(voir ci-dessous)* | Le mot de passe est généré au premier lancement |
| **Grafana** | http://localhost:3000 | `admin` | `dgssi_grafana` | Dashboard PostgreSQL + alertes de conformité |
| **Prometheus** | http://localhost:9090 | *(aucun)* | *(aucun)* | Pas d'authentification, accès direct |
| **Dashboard Flask** | http://localhost:5000 | *(aucun)* | *(aucun)* | Dashboard de conformité DGSSI |

### 🔐 Récupérer le mot de passe Airflow

Airflow en mode `standalone` génère un mot de passe aléatoire au premier démarrage. Pour le récupérer :

```powershell
docker logs dgssi-airflow 2>&1 | Select-String "password"
```

Cherchez la ligne qui contient : `Login with username: admin  password: XXXXXXXX`

---

## 4 — Ce qui a été fait et pourquoi

### ✅ Tâche 1 — Réparation d'Airflow

**Problème** : Airflow 2.10.5 crashait au démarrage à cause d'un conflit de versions SQLAlchemy.
- Airflow utilise **SQLAlchemy 1.4.x** en interne pour ses métadonnées
- Notre code Python (`dgssi_platform`) utilise **SQLAlchemy 2.x** (la classe `DeclarativeBase`)
- Installer les deux dans le même conteneur = crash immédiat

**Solution appliquée** : Architecture bi-couche
- Le **conteneur Airflow** n'installe **plus** SQLAlchemy 2.x → il orchestre seulement avec psycopg2 + dbt
- L'**extraction Docling** (qui a besoin de SQLAlchemy 2.x) s'exécute depuis le **venv local** sur la machine Windows
- Le script ETL (`etl_vers_warehouse.py`) utilise `psycopg2` directement → fonctionne dans Airflow sans conflit

**Fichiers modifiés** :
- `docker/airflow/Dockerfile` — Supprimé `sqlalchemy>=2.0`, ajouté `dbt-core` + `dbt-postgres`
- `airflow/dags/pipeline_conformite_dnssi.py` — Retiré la tâche `extraction_audit`, ajouté les variables d'environnement Docker

**Pourquoi cette approche ?**
- L'extraction Docling est un processus **ponctuel** (on ne reçoit pas 100 audits/jour)
- Installer PyTorch + Docling dans Docker prendrait **des heures** avec une connexion lente
- Séparer orchestration et exécution lourde est une **bonne pratique** en ingénierie des données

---

### ✅ Tâche 2 — Intégration dbt dans le DAG Airflow

**Ce qui est fait** : Le DAG Airflow exécute maintenant 3 tâches en chaîne :

```
etl_vers_warehouse → dbt_run → dbt_test
```

| Tâche | Ce qu'elle fait | Pourquoi |
|-------|----------------|----------|
| `etl_vers_warehouse` | Charge les données depuis MinIO Gold + tables opérationnelles vers le schéma étoile (warehouse) | Alimenter les dimensions et faits pour l'analyse |
| `dbt_run` | Exécute les 11 modèles dbt (staging + marts) | Transformer les données brutes en vues analytiques propres |
| `dbt_test` | Exécute les 37 tests dbt | Valider la qualité des données (unicité, non-null, relations) |

**Fichier** : `airflow/dags/pipeline_conformite_dnssi.py`

**Pourquoi dbt ?**
- **Reproductibilité** : chaque transformation est du SQL versionné dans Git
- **Tests automatiques** : 37 tests vérifient la qualité à chaque exécution
- **Documentation** : `dbt docs generate` produit un site web avec le lineage des données

---

### ✅ Tâche 3 — Monitoring avec Prometheus + Grafana

**Ce qui est fait** : Ajout de 3 conteneurs de monitoring qui surveillent PostgreSQL en continu.

| Conteneur | Rôle | Pourquoi |
|-----------|------|----------|
| **postgres-exporter** | Collecte les métriques PostgreSQL (connexions, transactions, locks, taille) et les expose au format Prometheus | PostgreSQL ne parle pas nativement le protocole Prometheus |
| **Prometheus** | Stocke les métriques toutes les 15 secondes, garde 7 jours d'historique | Base de données spécialisée pour les métriques temporelles |
| **Grafana** | Affiche les métriques sous forme de graphiques interactifs | Visualisation pro avec alerting intégré |

**Dashboard PostgreSQL créé** (`docker/grafana/provisioning/dashboards/postgres_dashboard.json`) :

Le dashboard contient **15 panneaux** organisés en 4 sections :

| Section | Panneaux | Ce que ça montre |
|---------|----------|------------------|
| 📊 Vue d'ensemble | Status PostgreSQL, Connexions actives, Taille base DGSSI, Transactions committées, Rollbacks, Locks actifs | Santé globale en un coup d'œil |
| 📈 Performance | Connexions par état, Transactions/seconde, Lignes lues/retournées, INSERT/UPDATE/DELETE par seconde | Performance des requêtes et charge |
| 💾 Cache & I/O | Cache Hit Ratio (jauge), Blocks cache vs disque | Efficacité du cache PostgreSQL (doit être > 95%) |
| 🔒 Locks & Deadlocks | Locks par mode, Deadlocks/seconde | Détection de problèmes de concurrence |

**Fichiers créés/modifiés** :
- `docker/prometheus/prometheus.yml` — Configuration des cibles à scraper
- `docker/grafana/provisioning/datasources/prometheus.yml` — Connexions Prometheus + PostgreSQL
- `docker/grafana/provisioning/dashboards/dashboard.yml` — Provider de dashboards
- `docker/grafana/provisioning/dashboards/postgres_dashboard.json` — **[NOUVEAU]** Dashboard complet

---

### ✅ Tâche 4 — Alerting automatique

**Ce qui est fait** : 2 alertes Grafana qui vérifient la conformité directement dans PostgreSQL.

#### Alerte 1 : Trop d'écarts critiques
| Paramètre | Valeur |
|-----------|--------|
| **Nom** | IIV — Trop d'écarts critiques |
| **Condition** | `nb_ecarts_critiques > 10` dans `public_marts.fact_conformite` |
| **Sévérité** | 🔴 Critical |
| **Fréquence** | Vérifié toutes les 5 minutes |
| **Action** | Envoie un POST JSON à `http://localhost:5000/api/alerts` (Dashboard Flask) |

**Pourquoi ?** : Un nombre élevé d'écarts critiques signifie qu'une IIV présente des failles de sécurité majeures par rapport à la DNSSI v2. La DGSSI doit être alertée immédiatement.

#### Alerte 2 : Taux de conformité trop bas
| Paramètre | Valeur |
|-----------|--------|
| **Nom** | IIV — Taux de conformité critique (< 50%) |
| **Condition** | `taux_conformite_global < 50` dans `public_marts.dim_audit` |
| **Sévérité** | 🟡 Warning |
| **Fréquence** | Vérifié toutes les 5 minutes |
| **Action** | Même webhook Flask |

**Pourquoi ?** : Un taux de conformité inférieur à 50% indique qu'une IIV ne respecte même pas la moitié des exigences DNSSI. C'est un signal d'alerte pour prioriser les actions correctives.

#### Notification Policy
Toutes les alertes avec le label `team: dgssi` sont envoyées au contact point `dgssi-webhook` qui fait un POST HTTP vers le dashboard Flask.

**Fichier** : `docker/grafana/provisioning/alerting/dgssi_alerts.yml`

---

## 5 — Guide d'utilisation pas à pas

### 🚀 Démarrage complet de la plateforme

```powershell
# Se placer dans le répertoire du projet
cd "~/OneDrive - um5.ac.ma/Bureau/dgssi-compilance - Copie"

# Lancer tous les services
docker compose up -d

# Vérifier que tout tourne
docker compose ps
```

Résultat attendu : **7 services UP** (postgres, minio, nifi, airflow, postgres-exporter, prometheus, grafana).

### 📄 Traiter un nouveau rapport d'audit

**Étape 1 : Déposer le PDF** dans MinIO via NiFi ou manuellement.

**Étape 2 : Extraction** (depuis le venv local, PAS dans Airflow) :
```powershell
# Activer le venv
.\venv\Scripts\Activate.ps1

# Lancer l'extraction
python scripts/extraire_audit_depuis_silver.py "Nom du rapport.pdf"
```

Cela fait : Bronze → Docling → Silver → Gold → PostgreSQL → Moteur de conformité.

**Étape 3 : Lancer le DAG Airflow** pour l'ETL + dbt :
- Ouvrir http://localhost:8085
- Activer le DAG `pipeline_conformite_dnssi` (toggle ON)
- Cliquer "Trigger DAG" (▶️)
- Ou en ligne de commande :
```powershell
docker exec dgssi-airflow airflow dags trigger pipeline_conformite_dnssi
```

**Étape 4 : Consulter les résultats**
- **Power BI** : Rafraîchir la connexion PostgreSQL
- **Dashboard Flask** : http://localhost:5000
- **Grafana** : http://localhost:3000

### 🔧 Exécuter dbt manuellement

```powershell
# Depuis le venv local
cd dbt_project

# Exécuter les modèles
dbt run

# Lancer les tests (37 tests)
dbt test

# Générer la documentation
dbt docs generate
dbt docs serve    # Ouvre un site web sur :8080
```

### 🔍 Vérifier le monitoring

1. **Prometheus** (http://localhost:9090) :
   - Aller dans Status → Targets
   - Vérifier que `postgres` et `prometheus` sont en état `UP`

2. **Grafana** (http://localhost:3000) :
   - Login : `admin` / `dgssi_grafana`
   - Dashboard : chercher "PostgreSQL — DGSSI Compliance"
   - Alertes : Alerting → Alert rules (2 règles actives)

### 🛑 Arrêter la plateforme

```powershell
# Arrêter tous les conteneurs (les données sont conservées dans les volumes)
docker compose stop

# Ou supprimer les conteneurs (les volumes persistent)
docker compose down

# Pour tout supprimer y compris les données
docker compose down -v
```

---

## 6 — Détail de chaque composant

### 📦 MinIO — Stockage objet (Architecture Medallion)

| Bucket | Contenu | Format |
|--------|---------|--------|
| `bronze` | PDF bruts déposés par NiFi | PDF original, non modifié |
| `silver` | Texte extrait + tableaux | `texte.md` + `tableaux.json` par document |
| `gold` | Données structurées prêtes pour PostgreSQL | JSON (audit complet avec chapitres, clauses, résultats) |
| `logs` | Logs de traitement | Fichiers texte |

**Pourquoi 3 couches ?** : Architecture Medallion — les données brutes (Bronze) ne sont jamais modifiées, ce qui permet de retraiter si l'algorithme d'extraction s'améliore.

### 🐘 PostgreSQL — Schéma de la base

**Tables opérationnelles** (créées par SQLAlchemy) :
- `audits` — Données principales de chaque audit
- `chapitres` — Chapitres DNSSI avec clauses identifiées
- `non_conformites` — Non-conformités détectées par chapitre
- `resultats_techniques` — Vulnérabilités par élément audité
- `evaluations_conformite` — Résultat du moteur de conformité
- `historique_versions` — Versioning des rapports

**Schéma warehouse** (créé par l'ETL) :
- `warehouse.dim_iiv` — Dimension IIV
- `warehouse.dim_prestataire` — Dimension prestataire d'audit
- `warehouse.dim_date` — Dimension temporelle
- `warehouse.dim_chapitre` — Dimension chapitres DNSSI
- `warehouse.dim_exigence` — Dimension exigences DNSSI
- `warehouse.dim_element_audite` — Dimension éléments techniques
- `warehouse.fait_evaluation_audit` — Faits d'évaluation
- `warehouse.fait_resultat_element` — Faits résultats techniques
- `warehouse.fait_clause_audit` — Faits clauses couvertes

**Vues dbt** (schéma `public_staging` et `public_marts`) :
- 11 modèles qui transforment les données en vues analytiques pour Power BI

### 🔧 dbt — Modèles et tests

```
dbt_project/models/
├── staging/          # Vues de nettoyage (renommage, typage)
│   ├── stg_audits.sql
│   ├── stg_chapitres.sql
│   └── ...
└── marts/            # Tables analytiques finales
    ├── dim_audit.sql
    ├── dim_chapitre_dnssi.sql
    ├── fact_conformite.sql
    ├── fact_chapitre_audit.sql
    └── fact_resultats_techniques.sql
```

**37 tests** vérifient :
- Unicité des clés primaires
- Non-nullité des champs obligatoires
- Intégrité référentielle entre les tables
- Cohérence des valeurs (taux entre 0 et 100, etc.)

### 🌬️ Airflow — DAG de pipeline

**DAG** : `pipeline_conformite_dnssi`

```
etl_vers_warehouse ──→ dbt_run ──→ dbt_test
```

| Tâche | Script | Durée typique |
|-------|--------|---------------|
| `etl_vers_warehouse` | `scripts/etl_vers_warehouse.py` | ~10s |
| `dbt_run` | `dbt run` (11 modèles) | ~15s |
| `dbt_test` | `dbt test` (37 tests) | ~10s |

**Planification** : `schedule=None` — déclenché manuellement. Pour planifier automatiquement, changer en `schedule="@daily"` ou `schedule="0 8 * * *"` (tous les jours à 8h).

---

## 7 — Dépannage courant

### Airflow ne démarre pas
```powershell
# Vérifier les logs
docker logs dgssi-airflow --tail 50

# Si erreur SQLAlchemy, vérifier la version
docker exec dgssi-airflow python -c "import sqlalchemy; print(sqlalchemy.__version__)"
# Doit afficher 1.4.x (PAS 2.x)
```

### Grafana en boucle de redémarrage
```powershell
# Vérifier les logs
docker logs dgssi-grafana --tail 20

# Si erreur de provisioning, recréer le volume
docker compose stop grafana
docker compose rm -f grafana
docker volume rm dgssi-compilance-copie_grafana_data
docker compose up -d grafana
```

### dbt test échoue
```powershell
# Voir le détail des tests en échec
cd dbt_project
dbt test --store-failures

# Les résultats sont stockés dans le schéma dbt_test_audit
```

### PostgreSQL : connexion refusée
```powershell
# Vérifier que le conteneur tourne
docker compose ps postgres

# Vérifier la santé
docker exec dgssi-postgres pg_isready -U dgssi
```

### Prometheus ne scrape pas PostgreSQL
```powershell
# Vérifier les targets
# Aller sur http://localhost:9090/targets
# Le target "postgres" doit être en état "UP"

# Si DOWN, vérifier postgres-exporter
docker logs dgssi-postgres-exporter --tail 20
```

---

## Fichiers modifiés dans cette session

| Fichier | Action | Description |
|---------|--------|-------------|
| `docker/airflow/Dockerfile` | Modifié | Supprimé SQLAlchemy 2.x, ajouté dbt-core + dbt-postgres |
| `airflow/dags/pipeline_conformite_dnssi.py` | Modifié | Retiré extraction_audit, ajouté variables d'environnement Docker |
| `docker/grafana/provisioning/datasources/prometheus.yml` | Modifié | Ajouté UID fixe, changé type vers grafana-postgresql-datasource |
| `docker/grafana/provisioning/alerting/dgssi_alerts.yml` | Modifié | Ajouté notification policy (route racine sans matchers) |
| `docker/grafana/provisioning/dashboards/postgres_dashboard.json` | **Créé** | Dashboard PostgreSQL complet (15 panneaux) |

---

> **💡 Conseil** : Ce fichier est votre référence principale. Gardez-le à jour au fur et à mesure de l'évolution de la plateforme.
