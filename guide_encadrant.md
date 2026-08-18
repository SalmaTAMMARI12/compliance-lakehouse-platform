# Guide opérationnel — Plateforme de conformité DGSSI / DNSSI v2

**Auteur :** Salma TAMMARI — Stage ingénieure DGSSI, été 2026  
**Stack :** Python 3.11 · Docker · PostgreSQL 16 · MinIO · Apache NiFi · Apache Airflow · dbt · Prometheus · Grafana · Flask

---

## Table des matières

1. [Prérequis](#1--prérequis)
2. [Installation](#2--installation)
3. [Configuration (.env)](#3--configuration-env)
4. [Modèle LLM — téléchargement obligatoire](#4--modèle-llm--téléchargement-obligatoire)
5. [Lancement des services Docker](#5--lancement-des-services-docker)
6. [URLs d'accès et identifiants](#6--urls-daccès-et-identifiants)
7. [Initialisation de la base de données](#7--initialisation-de-la-base-de-données)
8. [Créer les buckets MinIO](#8--créer-les-buckets-minio)
9. [Déposer et traiter un rapport d'audit](#9--déposer-et-traiter-un-rapport-daudit)
10. [Lancer le dashboard](#10--lancer-le-dashboard)
11. [Lancer le pipeline Airflow (ETL + dbt)](#11--lancer-le-pipeline-airflow-etl--dbt)
12. [Scripts disponibles](#12--scripts-disponibles)
13. [Dépannage courant](#13--dépannage-courant)
14. [Architecture](#14--architecture)

---

## 1 — Prérequis

| Outil | Version minimale | Vérification |
|---|---|---|
| Python | 3.11 | `python --version` |
| Docker Desktop | 4.x | `docker --version` |
| Docker Compose | v2 | `docker compose version` |
| Git | 2.x | `git --version` |
| RAM disponible | 8 Go recommandés | — |
| Espace disque libre | 10 Go | — |

> **Important** : Docker Desktop doit être **lancé et démarré** avant toute commande `docker compose`.

---

## 2 — Installation

### 2.1 Cloner le dépôt

```powershell
git clone <url_du_depot>
cd "dgssi-compilance - MultiAudit"
```

### 2.2 Créer l'environnement virtuel Python

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2.3 Installer le projet et ses dépendances

```powershell
pip install -e ".[database,storage,extraction]"
pip install -r requirements.txt
```

> Si `pip install -e` échoue, essaie d'abord : `pip install hatchling` puis relance.

---

## 3 — Configuration (.env)

Copie le fichier modèle et renseigne les valeurs :

```powershell
copy .env.example .env
```

Ouvre `.env` et remplis :

```dotenv
APP_ENV=dev
LOG_LEVEL=INFO

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=dgssi
POSTGRES_USER=dgssi
POSTGRES_PASSWORD=changeme

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=dgssi_admin
MINIO_SECRET_KEY=changeme123
MINIO_BUCKET_BRONZE=bronze
MINIO_BUCKET_SILVER=silver
MINIO_BUCKET_GOLD=gold
MINIO_BUCKET_LOGS=logs

# LLM (chemin absolu vers le fichier .gguf)
LLM_MODEL_PATH=C:/chemin/vers/qwen2.5-1.5b-instruct-q4_k_m.gguf
```

---

## 4 — Modèle LLM — téléchargement obligatoire

Le pipeline utilise un LLM local (Qwen 2.5 1.5B) pour extraire le texte libre des rapports. **Ce fichier n'est pas dans le dépôt** (environ 900 Mo).

**Etape 1 — Télécharger le modèle :**

```
https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
```

> Copie-colle l'URL dans ton navigateur, le téléchargement démarre automatiquement.

**Etape 2 — Renseigner le chemin dans `.env` :**

```dotenv
LLM_MODEL_PATH=C:/Users/ton_nom/Downloads/qwen2.5-1.5b-instruct-q4_k_m.gguf
```

> Utilise des `/` (slashs normaux), pas des `\`, même sur Windows.

---

## 5 — Lancement des services Docker

### Démarrer tous les services

```powershell
docker compose up -d
```

Cela lance **6 conteneurs** :

| Conteneur | Role |
|---|---|
| `dgssi-postgres` | Base de données PostgreSQL 16 |
| `dgssi-minio` | Lac de données objet (Bronze/Silver/Gold) |
| `dgssi-nifi` | Ingestion automatique des rapports |
| `dgssi-airflow` | Orchestrateur (ETL + dbt) |
| `dgssi-prometheus` | Collecte des métriques |
| `dgssi-grafana` | Dashboard de monitoring |

### Vérifier que tout tourne

```powershell
docker compose ps
```

Tous les services doivent être en état `running` (ou `healthy`).

### Arrêter les services

```powershell
docker compose down
```

### Arrêter et supprimer les données (reset complet)

```powershell
docker compose down -v
```

---

## 6 — URLs d'accès et identifiants

| Service | URL | Login | Mot de passe |
|---|---|---|---|
| **MinIO** (console web) | http://localhost:9001 | `dgssi_admin` | `changeme123` |
| **MinIO** (API S3) | http://localhost:9000 | — | — |
| **NiFi** (interface de flux) | https://localhost:8443/nifi | `admin` | `dgssiAdmin123!` |
| **Airflow** (orchestrateur) | http://localhost:8085 | `admin` | `admin` |
| **Grafana** (monitoring) | http://localhost:3000 | `admin` | `dgssi_grafana` |
| **Prometheus** (métriques brutes) | http://localhost:9090 | — | — |
| **Dashboard Flask** | http://localhost:5000 | — | — |
| **PostgreSQL** (connexion directe) | `localhost:5432` | `dgssi` | `changeme` |

> **NiFi** utilise **HTTPS** (pas HTTP). Le navigateur affichera un avertissement de certificat auto-signé — clique sur "Avancer quand même" (Chrome) ou "Accepter le risque" (Firefox).

> **Airflow** : au premier démarrage, le compte `admin/admin` est créé automatiquement. Pour le voir dans les logs : `docker logs dgssi-airflow | findstr "password"`.

---

## 7 — Initialisation de la base de données

A faire **une seule fois** après le premier `docker compose up` :

```powershell
# Active d'abord le venv si ce n'est pas déjà fait
.\venv\Scripts\activate

# Crée toutes les tables dans PostgreSQL
python -c "
from dgssi_platform.infrastructure.database.models.audit_model import Base
from sqlalchemy import create_engine
from dgssi_platform.shared.config import get_settings
engine = create_engine(get_settings().postgres_dsn)
Base.metadata.create_all(engine)
print('Tables créées avec succès.')
"
```

---

## 8 — Créer les buckets MinIO

A faire **une seule fois** après le premier démarrage.

**Option A — Via l'interface web :**

1. Ouvre http://localhost:9001
2. Connecte-toi avec `dgssi_admin` / `changeme123`
3. Clique sur **"Buckets"** puis **"Create Bucket"**
4. Crée les 4 buckets suivants (un par un) :
   - `bronze`
   - `silver`
   - `gold`
   - `logs`

**Option B — En ligne de commande (si `mc` est installé) :**

```powershell
mc alias set minio http://localhost:9000 dgssi_admin changeme123
mc mb minio/bronze minio/silver minio/gold minio/logs
```

---

## 9 — Déposer et traiter un rapport d'audit

### Etape 1 — Déposer le rapport dans Bronze (MinIO)

1. Ouvre http://localhost:9001
2. Va dans le bucket **`bronze`**
3. Clique **Upload** et sélectionne ton fichier PDF ou DOCX

### Etape 2 — Lancer le parsing (Bronze → Silver)

```powershell
.\venv\Scripts\activate

# Pour un fichier PDF (utilise Docling — peut prendre 2-5 minutes)
python scripts\parser_vers_silver.py "data\private\mon_rapport.pdf"

# Pour un fichier DOCX (python-docx — environ 5 secondes)
python scripts\parser_vers_silver.py "data\private\mon_rapport.docx"
```

> Apres cette étape, le bucket **Silver** de MinIO contient :
> - `silver/<nom_rapport>/texte.md` — le texte extrait en Markdown
> - `silver/<nom_rapport>/tableaux.json` — les tableaux structurés

### Etape 3 — Lancer le pipeline principal (Silver → Gold → PostgreSQL)

```powershell
python scripts\executer_pipeline_complet.py "nom_rapport_sans_extension"
```

**Exemple :**

```powershell
python scripts\executer_pipeline_complet.py "Exemple de rapport d'audit"
```

Le pipeline exécute 4 étapes en séquence :
1. Lit le texte depuis Silver (MinIO)
2. Extrait les données via Regex + LLM (2 à 5 minutes selon la taille du rapport)
3. Sauvegarde le résultat JSON dans Gold (MinIO)
4. Enregistre l'audit dans PostgreSQL

**Sortie attendue :**

```
============================================================
Pipeline DGSSI — rapport : Exemple de rapport d'audit
============================================================

[1/4] Lecture depuis Silver...
      OK — texte: 85432 caractères, 47 tableaux

[2/4] Extraction (regex + LLM local, patientez — plusieurs minutes)...
      OK — taux: 68% | chapitres: 14 | non-conformités: 19

[3/4] Sauvegarde Gold (MinIO)...
      OK — gold/Exemple de rapport d'audit.json mis à jour

[4/4] Sauvegarde PostgreSQL...
      OK — audit_id=1
============================================================
```

---

## 10 — Lancer le dashboard

```powershell
.\venv\Scripts\activate
python dashboard.py
```

Ouvre ensuite : **http://localhost:5000**

Le dashboard affiche :
- Taux de conformité global par audit
- Liste des non-conformités par chapitre DNSSI
- Périmètres fonctionnels et techniques
- Résultats des tests techniques
- KPIs : nombre d'écarts critiques, éléments les plus exposés

---

## 11 — Lancer le pipeline Airflow (ETL + dbt)

Cette étape transforme les données PostgreSQL en schéma analytique (étoile).  
A lancer **après** avoir traité au moins un rapport (étape 9).

1. Ouvre http://localhost:8085
2. Connecte-toi avec `admin` / `admin`
3. Recherche le DAG **`pipeline_conformite_dnssi`**
4. Active le DAG (toggle en haut à gauche)
5. Clique **Trigger DAG** pour le lancer manuellement

Le DAG exécute 3 tâches en séquence :

```
etl_vers_warehouse  ->  dbt_run  ->  dbt_test
     (~10s)             (~15s)        (~10s)
```

| Tâche | Ce qu'elle fait |
|---|---|
| `etl_vers_warehouse` | Charge les données de PostgreSQL opérationnel vers le schéma étoile (warehouse) |
| `dbt_run` | Exécute les 11 modèles dbt (vues analytiques pour Power BI) |
| `dbt_test` | Vérifie les 37 tests de qualité (unicité, intégrité référentielle, valeurs valides) |

> En cas d'échec : clique sur la tâche rouge puis "Log" pour voir l'erreur détaillée.

### Lancer dbt manuellement (sans Airflow)

```powershell
cd dbt_project
dbt run --profiles-dir . --project-dir .
dbt test --profiles-dir . --project-dir .
```

---

## 12 — Scripts disponibles

| Script | Usage | Description |
|---|---|---|
| `scripts\executer_pipeline_complet.py` | `python scripts\executer_pipeline_complet.py "nom"` | Pipeline principal : Silver -> Gold -> PostgreSQL |
| `scripts\parser_vers_silver.py` | `python scripts\parser_vers_silver.py "chemin\fichier.pdf"` | Parse un fichier local et dépose dans Silver |
| `scripts\extraire_audit_depuis_silver.py` | `python scripts\extraire_audit_depuis_silver.py "fichier.pdf"` | Pipeline complet avec Docling (Bronze -> PostgreSQL) |
| `scripts\etl_vers_warehouse.py` | `python scripts\etl_vers_warehouse.py` | ETL manuel vers le warehouse (schéma étoile) |
| `scripts\re_sauvegarder_db.py` | `python scripts\re_sauvegarder_db.py` | Recharge les audits Gold dans PostgreSQL (utile après un reset DB) |
| `scripts\fast_fix.py` | `python scripts\fast_fix.py` | Corrige les périmètres manquants via LLM pour les rapports déjà traités |
| `scripts\comparer_parseurs.py` | `python scripts\comparer_parseurs.py "chemin\fichier.pdf"` | Benchmark : compare Docling, pdfplumber, pymupdf sur un rapport |
| `scripts\lister_tables.py` | `python scripts\lister_tables.py` | Liste les tables existantes dans PostgreSQL |
| `dashboard.py` | `python dashboard.py` | Lance le dashboard Flask sur http://localhost:5000 |

---

## 13 — Dépannage courant

### Erreur : modèle LLM introuvable

```
Modèle LLM introuvable : ...
```

Vérifie que `LLM_MODEL_PATH` dans `.env` pointe vers le fichier `.gguf` téléchargé.  
Utilise des `/` (pas des `\`).  
Vérifie que le fichier existe : `Test-Path "C:/chemin/vers/fichier.gguf"`

---

### Erreur : connexion refusée sur PostgreSQL

```
psycopg2.OperationalError: connection to server at "localhost" failed
```

Vérifie que le conteneur tourne : `docker compose ps`  
Relance si nécessaire : `docker compose up -d postgres`  
Teste la connexion : `docker exec dgssi-postgres pg_isready -U dgssi`

---

### MinIO : bucket introuvable

```
NoSuchBucket: The specified bucket does not exist
```

Les 4 buckets ne sont pas créés. Suis la section 8.

---

### NiFi : avertissement de sécurité dans le navigateur

C'est normal (certificat TLS auto-signé). Clique sur "Avancer quand même" (Chrome) ou "Accepter le risque" (Firefox).

---

### Airflow ne démarre pas ou boucle en redémarrage

```powershell
docker logs dgssi-airflow --tail 50
```

Si erreur SQLAlchemy : vérifie que PostgreSQL est bien démarré avant Airflow.  
Si erreur de port : `8085` est peut-être utilisé par une autre application. Modifie le port dans `docker-compose.yaml`.

---

### Grafana en boucle de redémarrage

```powershell
docker logs dgssi-grafana --tail 20
docker compose stop grafana
docker compose rm -f grafana
docker volume rm dgssi-grafana-data
docker compose up -d grafana
```

---

### Le pipeline LLM est lent

C'est attendu sur CPU sans GPU. Compter 2 à 5 minutes par rapport selon sa taille.  
Le modèle Qwen 1.5B s'exécute entièrement en local, sans connexion internet.

---

### ModuleNotFoundError : dgssi_platform

L'environnement virtuel n'est pas activé ou le package n'est pas installé.

```powershell
.\venv\Scripts\activate
pip install -e ".[database,storage,extraction]"
```

---

## 14 — Architecture

Le schéma ci-dessous présente l'architecture complète de la plateforme : sources d'entrée, data lakehouse MinIO (Bronze / Silver / Gold), pipeline d'extraction hybride (Regex + LLM), stockage et entrepôt (PostgreSQL + dbt), restitution (Flask + Grafana) et orchestration (Airflow + Docker).

![Architecture technique de la plateforme DGSSI](C:\Users\hp\.gemini\antigravity-ide\brain\36999399-bc23-41b2-b868-a2debc58b767\archi.png)

---

## Récapitulatif des identifiants

| Service | URL | Login | Mot de passe |
|---|---|---|---|
| MinIO Console | http://localhost:9001 | `dgssi_admin` | `changeme123` |
| NiFi | https://localhost:8443/nifi | `admin` | `dgssiAdmin123!` |
| Airflow | http://localhost:8085 | `admin` | `admin` |
| Grafana | http://localhost:3000 | `admin` | `dgssi_grafana` |
| PostgreSQL | `localhost:5432` db=`dgssi` | `dgssi` | `changeme` |
| Dashboard Flask | http://localhost:5000 | — | — |
| Prometheus | http://localhost:9090 | — | — |
