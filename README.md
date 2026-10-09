
# AuditDataPlatform — Plateforme Data d'Audit Automatisé

Ce projet met en place une plateforme de données complète qui automatise le traitement des rapports d'audit de conformité des Infrastructures d'Importance Vitale (IIV) au référentiel national **DNSSI v2**.

La plateforme repose sur un pipeline ELT qui :

- **Ingère les données** à partir de rapports d'audit PDF et DOCX via Apache NiFi.
- **Stocke les documents** dans MinIO selon une architecture Data Lake en zones Bronze, Silver et Gold.
- **Extrait les informations** grâce à une approche hybride combinant un LLM local (Qwen 2.5) et des expressions régulières.
- **Transforme les données** dans PostgreSQL avec dbt, selon un schéma en étoile.
- **Contrôle la qualité** des données grâce à des tests automatisés dbt.
- **Orchestre les traitements** avec Apache Airflow.
- **Supervise l'infrastructure** avec Prometheus et Grafana.
- **Visualise les résultats** dans un tableau de bord développé avec Flask.

---

## Table des matières

1. [Architecture du Pipeline](#architecture-du-pipeline)
2. [Démonstration du Dashboard](#démonstration-du-dashboard)
3. [Stack Technologique](#stack-technologique)
4. [Services Docker](#services-docker)
5. [Lancement du Projet](#lancement-du-projet)

---

## Architecture du Pipeline

Voici l'architecture globale de la solution :
<img width="1629" height="966" alt="arch-finaaal" src="https://github.com/user-attachments/assets/68c5ff3d-e070-471a-8907-086c821339c5" />

- **Ingestion** : Apache NiFi détecte et prend en charge les nouveaux rapports.
- **Stockage** : MinIO conserve les documents originaux et les données intermédiaires.
- **Extraction** : Docling et python-docx permettent de traiter les documents, puis Qwen 2.5 et les expressions régulières extraient les informations utiles.
- **Transformation** : dbt prépare les données analytiques dans PostgreSQL.
- **Orchestration** : Apache Airflow coordonne les différentes étapes du pipeline.
- **Visualisation** : Flask présente les résultats et les indicateurs de conformité.

---

## Démonstration du Dashboard

Voici une capture d'écran du tableau de bord final de la plateforme :

<img width="1508" height="687" alt="Capture d&#39;écran 2026-10-09 134452" src="https://github.com/user-attachments/assets/78fff55b-7747-4040-af13-029b6a59cb37" />

Le dashboard permet de consulter :

- Une vue générale des indicateurs de conformité.
- Les résultats des audits organisationnels et techniques.
- Les constats et les non-conformités détectés.
- La traçabilité des données extraites par le LLM.
- L'historique des versions des audits.

---

## Stack Technologique

| Composant | Technologies |
|---|---|
| Ingestion | Apache NiFi 1.27 |
| Stockage objet | MinIO (compatible S3) |
| Parsing documentaire | Docling, python-docx |
| Intelligence artificielle | Qwen 2.5, llama-cpp-python |
| Extraction déterministe | Python, expressions régulières |
| Data Warehouse | PostgreSQL 16 |
| Transformation | dbt Core |
| Qualité des données | Tests automatisés dbt |
| Orchestration | Apache Airflow 2.10 |
| Dashboard | Flask |
| Monitoring | Prometheus, Grafana, cAdvisor |
| Conteneurisation | Docker Compose |

---

## Services Docker

L'infrastructure est conteneurisée avec Docker Compose et comprend les services suivants :

- PostgreSQL
- MinIO
- Apache NiFi
- Apache Airflow
- Worker de traitement documentaire
- Prometheus
- Grafana
- PostgreSQL Exporter
- cAdvisor

---

## Lancement du Projet

### 1. Configurer l'environnement

```bash
cp .env.example .env
```

Configurer les variables d'environnement nécessaires, notamment le chemin vers le modèle LLM local au format GGUF.

### 2. Démarrer l'infrastructure

```bash
docker compose up -d
```

### 3. Exécuter le pipeline sur un rapport

```bash
python scripts/executer_pipeline_complet.py --rapport data/private/rapport.pdf
```

### 4. Lancer le tableau de bord

```bash
python dashboard.py
```

Le dashboard est accessible à l'adresse :

http://localhost:5000

### 5. Accéder aux services

- **Dashboard Flask** : http://localhost:5000
- **Airflow** : http://localhost:8085
- **Grafana** : http://localhost:3000
- **MinIO** : http://localhost:9001

---

## Chiffres Clés

| Indicateur | Valeur |
|---|---|
| Exigences du référentiel DNSSI v2 | 104 |
| Tests de qualité dbt | 65 |
| Extracteurs Regex spécialisés | 14 |
| Extracteurs LLM spécialisés | 7 |
| Formats d'entrée supportés | PDF, DOCX |
| Services Docker | 9 |

---

## Auteur

**Salma TAMMARI**
Élève ingénieure à l'ENSIAS  
Projet de Fin d'Année — DGSSI  
Division Contrôle et Expertise  
