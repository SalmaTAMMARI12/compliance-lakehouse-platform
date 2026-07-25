# 🎯 Présentation du Projet — Réunion DGSSI

## Intitulé

**Conception et mise en œuvre d'une plateforme d'ingénierie et d'analyse des données réglementaires pour l'évaluation automatisée de la conformité des IIV aux normes DNSSI v2**

---

## 1 — Le problème qu'on résout

La DGSSI reçoit des rapports d'audit PDF de la part des IIV. Ces rapports font souvent **50 à 100+ pages**. Aujourd'hui, un analyste doit :
- Lire chaque rapport manuellement
- Identifier les 14 chapitres DNSSI v2 couverts
- Repérer les non-conformités et les vulnérabilités techniques
- Calculer le taux de conformité
- Comparer avec les exigences réglementaires
- Produire un compte-rendu

**→ C'est long, subjectif, et pas reproductible.**

Notre plateforme fait tout ça **automatiquement** : on dépose un PDF, et en quelques minutes on obtient le taux de conformité, les écarts critiques, les équipements les plus exposés, et des tableaux de bord prêts à l'emploi.

---

## 2 — Comment fonctionne la plateforme (en simple)

```
📄 Rapport d'audit PDF (ex: "Rapport d'audit IIV_A")
        │
        ▼
   ┌─────────────┐
   │  1. NiFi     │  ← Récupère le PDF automatiquement
   │  (Ingestion) │    et le dépose dans MinIO
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │  2. MinIO    │  ← Stockage en 3 couches :
   │  (Stockage)  │    Bronze (PDF brut)
   │              │    Silver (texte + tableaux extraits)
   │              │    Gold (données structurées JSON)
   └──────┬──────┘
          ▼
   ┌─────────────────────────────────┐
   │  3. Python + Docling + LLM      │  ← Extraction intelligente :
   │  (Extraction)                    │    • Docling parse le PDF
   │                                  │    • Regex capture les tableaux
   │                                  │    • LLM comprend le texte libre
   └──────┬──────────────────────────┘
          ▼
   ┌─────────────┐
   │  4. Postgres │  ← Stockage structuré en étoile :
   │  (Base)      │    dimensions + faits
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │  5. dbt      │  ← Transformation et validation :
   │  (Transform) │    11 modèles, 37 tests qualité
   └──────┬──────┘
          ▼
   ┌─────────────────────────────────┐
   │  6. Power BI + Flask + Grafana   │  ← Visualisation :
   │  (Dashboards)                    │    Tableaux de bord décisionnels
   └──────────────────────────────────┘
```

---

## 3 — Ce que la plateforme extrait du rapport (exemple réel)

### Rapport traité : audit de conformité DNSSI d'une IIV

Voici ce que notre système a extrait **automatiquement** du PDF :

### 3.1 — Informations générales de l'audit

| Champ | Valeur extraite | Méthode |
|-------|-----------------|---------|
| Nom de l'IIV | IIV_A | Regex |
| Secteur | inconnu | Regex |
| Prestataire d'audit | PASSI FFFFFF | Regex |
| Classification | Confidentiel | Regex |
| Taux de conformité global | **76.7%** | Regex (tableau §2.3) |
| Confiance de l'extraction | 94% | Calculé |
| Écarts par type | 11 significatifs, 7 non-significatifs, 1 remarque | Regex (tableau §2.3) |

### 3.2 — Périmètre audité (extrait automatiquement)

**Périmètre fonctionnel** (§1.1 du rapport) :
- Les Systèmes d'Information métier
- Les systèmes support (Messagerie, Active Directory, etc.)
- L'infrastructure réseaux et sécurité
- Le Datacenter

**Périmètre technique** (§4.1 du rapport) :
- Le firewall central Forcepoint
- Le firewall Fortigate partenaire
- Le firewall Fortigate frontal
- Le switch fédérateur
- Le serveur de messagerie
- Le serveur web alpha

### 3.3 — Les 14 chapitres DNSSI v2 et leurs clauses (extrait par LLM + Regex)

Le rapport couvre les 14 chapitres de la DNSSI v2. Pour chaque chapitre, notre système identifie les **codes de clauses** applicables :

| # | Chapitre DNSSI v2 | Nb clauses | Exemples de codes |
|---|-------------------|------------|-------------------|
| 1 | Politique de sécurité des SI | 4 | POL-RISQUE, POL-FORMEL, POL-PAS, POL-TDB |
| 2 | Organisation de la sécurité des SI | 4 | ORG-INTER-GOUV, ORG-INTER-RSSI |
| 3 | Sécurité des ressources humaines | 4 | RH-AVT-PERSON, RH-APRES-FORM |
| 4 | Gestion des actifs informationnels | 11 | ACTIF-RESP-INV, ACTIF-CLASSIF-INFO |
| 5 | Contrôle d'accès | 9 | ACC-EXIG-POL, ACC-UTILIS-MDP |
| 6 | Cryptographie | 2 | CRYPTO-MES-POL, CRYPTO-MES-GESTCLE |
| 7 | Sécurité physique et environnementale | 12 | PHYS-ZONE-DELIMIT, PHYS-MAT-CLIM |
| 8 | Sécurité liée à l'exploitation | 19 | EXP-PROC-CHANG, EXP-VULN-GEST |
| 9 | Sécurité des communications | 9 | COM-MANAG-FILTRAGE, COM-TRANS-MESS |
| 10 | Acquisition, développement, maintenance | 8 | DEV-EXIG-PROJET, DEV-PROC-CODE |
| 11 | Relations avec les fournisseurs | 4 | FOURNIS-REL-RISQ, FOURNIS-GEST-SURVEIL |
| 12 | Gestion des incidents de cybersécurité | 8 | INCID-GEST-PROC, INCID-GEST-ALERT |
| 13 | Continuité d'activité | 4 | CONTINU-BIA, CONTINU-EXERCICE |
| 14 | Conformité | 6 | CONF-OBLIG-IDF, CONF-REVU-SSI |

**Total : 104 clauses identifiées automatiquement** dans ce seul rapport.

### 3.4 — Résultats techniques par équipement (extrait par Regex des tableaux)

| Équipement audité | Critique 🔴 | Élevée 🟠 | Moyenne 🟡 | Faible 🟢 | **Score total** |
|-------------------|:-----------:|:---------:|:----------:|:---------:|:---------------:|
| Architecture | 0 | 0 | 3 | 2 | 5 |
| Firewall Central Forcepoint | 2 | 0 | 5 | 1 | 8 |
| Firewall Partenaire | 3 | 4 | 9 | 1 | 17 |
| Firewall Frontal | 3 | 4 | 9 | 1 | 17 |
| Switch fédérateur | 2 | 2 | 7 | 1 | 12 |
| Serveur de messagerie | 0 | 16 | 6 | 2 | 24 |
| **Serveur web Alpha** | **6** | **14** | **7** | **0** | **27** ⚠️ |

→ Le **serveur web Alpha** est l'élément **le plus exposé** avec 6 vulnérabilités critiques et un score total de 27.

### 3.5 — Non-conformités (extraites par LLM)

Exemples de non-conformités détectées automatiquement par le LLM (avec confiance 70%) :

| Chapitre | Constat résumé | Méthode |
|----------|----------------|---------|
| Politique de sécurité | Plan d'action annuel global de la sécurité SI et suivi régulier | LLM |
| Politique de sécurité | Feuille de route sécurité 2024-2026 élaborée avec projets et budget | LLM |
| Politique de sécurité | Indicateurs de suivi régulièrement générés pour conformité et gouvernance | LLM |
| *... et d'autres pour chaque chapitre* | | |

---

## 4 — Comment les données sont structurées (schéma en étoile)

### 4.1 — Pourquoi un schéma en étoile ?

Un schéma en étoile sépare les **faits** (mesures, scores, comptages) des **dimensions** (contexte : qui, quoi, quand). C'est le standard pour l'analyse décisionnelle car :
- Power BI et les outils BI sont optimisés pour ce modèle
- Les requêtes analytiques sont simples et rapides
- On peut croiser facilement les données selon n'importe quel axe

### 4.2 — Les tables dimensions (le contexte)

```
┌──────────────────────┐     ┌──────────────────────┐
│   dim_audit           │     │   dim_iiv             │
├──────────────────────┤     ├──────────────────────┤
│ audit_id (PK)         │     │ iiv_key (PK)          │
│ iiv_key (FK)          │────→│ iiv_nom               │
│ prestataire_audit     │     │ iiv_secteur           │
│ classification        │     └──────────────────────┘
│ taux_conformite_global│
│ date_extraction       │     ┌──────────────────────┐
│ confiance_extraction  │     │ dim_chapitre_dnssi    │
│ nb_ecarts_par_type    │     ├──────────────────────┤
│ perimetre_fonctionnel │     │ chapitre_dnssi_id (PK)│
│ perimetre_technique   │     │ code_chapitre (CH01…) │
└──────────────────────┘     │ nom_chapitre          │
                              │ domaine               │
                              └──────────────────────┘
```

| Dimension | Ce qu'elle contient | Combien de lignes |
|-----------|--------------------|--------------------|
| `dim_audit` | Un audit = une IIV auditée à une date donnée | 1 par audit reçu |
| `dim_iiv` | Identité de l'IIV (nom, secteur) | 1 par IIV unique |
| `dim_chapitre_dnssi` | Les 14 chapitres du référentiel DNSSI v2 | **Toujours 14** (fixe) |

### 4.3 — Les tables de faits (les mesures)

| Table de faits | Ce qu'elle mesure | Grain (1 ligne = ?) |
|----------------|-------------------|---------------------|
| `fact_conformite` | Taux de conformité, nb écarts critiques, statut | 1 évaluation par audit |
| `fact_resultats_techniques` | Vulnérabilités par équipement (critique, élevée, moyenne, faible) + score pondéré | 1 équipement dans 1 audit |
| `fact_chapitre_audit` | Quel chapitre DNSSI a été couvert, avec quelles clauses | 1 chapitre dans 1 audit |
| `fact_non_conformite` | Constats de non-conformité extraits (texte, recommandation, confiance) | 1 non-conformité |

### 4.4 — Schéma en étoile visuel

```
                         ┌─────────────────┐
                         │   dim_iiv        │
                         │ (IIV_A, IIV_B…)  │
                         └────────┬────────┘
                                  │
┌──────────────────┐    ┌────────┴────────┐    ┌──────────────────┐
│ dim_chapitre_    │    │                  │    │                  │
│ dnssi            │    │    dim_audit     │    │ fact_conformite  │
│ (14 chapitres    │◄───│  (1 par audit)   │───►│ (taux, écarts,   │
│  DNSSI v2)       │    │                  │    │  statut)         │
└──────────────────┘    └───────┬──────────┘    └──────────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│ fact_chapitre_   │    │ fact_resultats_  │
│ audit            │    │ techniques       │
│ (chapitre ×      │    │ (vulnérabilités  │
│  audit + clauses)│    │  par équipement) │
└──────────────────┘    └──────────────────┘
        │
        ▼
┌──────────────────┐
│ fact_non_        │
│ conformite       │
│ (constats LLM)   │
└──────────────────┘
```

---

## 5 — L'extraction intelligente : LLM + Regex

### 5.1 — Pourquoi deux méthodes ?

| Donnée à extraire | Méthode | Pourquoi |
|-------------------|---------|----------|
| Nom IIV, prestataire, classification | **Regex** | Toujours au même endroit dans le rapport (page de garde, §1) |
| Taux de conformité, écarts par type | **Regex** | Tableau structuré au §2.3, format fixe |
| Résultats techniques (critique/élevée/moyenne/faible) | **Regex** | Tableau du §4 avec colonnes bien définies |
| Clauses DNSSI par chapitre (POL-RISQUE, ACC-MDP…) | **Regex + LLM** | Les codes sont dans le texte mais parfois mal formatés |
| Non-conformités, constats, recommandations | **LLM** | Texte libre, reformulé par l'auditeur, impossible avec du Regex |
| Périmètre fonctionnel et technique | **LLM** | Phrases en langage naturel |

### 5.2 — Comment ça marche concrètement

```python
# 1. Docling parse le PDF en texte structuré + tableaux
document = DoclingParseur().parser("rapport.pdf")
# → document.texte = texte markdown complet
# → document.tableaux = liste de tableaux avec lignes/colonnes

# 2. L'ExtracteurHybride combine Regex + LLM
audit = ExtracteurHybride().extraire(document)
# → Regex : capture taux, tableaux, codes de clauses
# → LLM : comprend les non-conformités en texte libre

# 3. Le moteur de conformité évalue
evaluation = evaluer_conformite_globale(audit)
# → Statut : CONFORME / NON_CONFORME / PARTIELLEMENT_CONFORME
# → Nb écarts critiques, élément le plus exposé
```

### 5.3 — Confiance de l'extraction

Chaque extraction a un **score de confiance** (0 à 1) :

| Catégorie | Confiance | Signification |
|-----------|-----------|---------------|
| Classification | 1.0 (100%) | Trouvé exactement par Regex |
| Taux de conformité | 1.0 (100%) | Tableau parsé sans ambiguïté |
| Résultats techniques | 1.0 (100%) | Tableau structuré |
| Historique versions | 0.9 (90%) | Regex fiable mais format variable |
| Prestataire | 0.9 (90%) | Regex sur la page de garde |
| Clauses DNSSI | 1.0 (100%) | Codes identifiés dans les titres |
| **Non-conformités (LLM)** | **0.7 (70%)** | **Texte libre, interprétation IA** |
| **Confiance globale** | **0.94 (94%)** | **Moyenne pondérée** |

Les non-conformités extraites par LLM avec confiance < 80% sont marquées `a_verifier = true` → un analyste humain doit les valider avant de les exploiter.

### 5.4 — Généralisation à tous les rapports

Le système est conçu pour traiter **tous types de rapports** listés dans la fiche de projet :

| Type de rapport | Support actuel | Ce qu'il faut adapter |
|----------------|----------------|----------------------|
| ✅ Audit conformité DNSSI v2 | **Fonctionnel** | — |
| 🔲 Audit de configuration | Même pipeline | Adapter les Regex pour les tableaux de config |
| 🔲 Audit d'architecture | Même pipeline | Adapter l'extraction LLM pour les schémas d'archi |
| 🔲 Tests d'intrusion (Pentest) | Même pipeline | Regex pour les CVE, LLM pour les recommandations |
| 🔲 Dossiers d'homologation | Même pipeline | Adapter les dimensions (échéances, systèmes) |

L'architecture est **extensible** : pour chaque nouveau type de rapport, on ajoute des extracteurs spécialisés sans changer le pipeline.

---

## 6 — Les KPIs réglementaires produits

| KPI | Comment il est calculé | Table source | Exemple |
|-----|----------------------|--------------|---------|
| **Taux global de conformité** | Extrait directement du rapport (§2.3) | `dim_audit.taux_conformite_global` | 76.7% |
| **Nb écarts critiques** | Somme des vulnérabilités "critique" par équipement | `fact_resultats_techniques.critique` | 16 |
| **Nb écarts par type** | Significatif / Non-significatif / Remarque | `dim_audit.nb_ecarts_par_type` | 11 / 7 / 1 |
| **Score d'exposition pondéré** | critique×4 + élevée×3 + moyenne×2 + faible×1 | `fact_resultats_techniques.score_exposition_pondere` | Serveur web: 69 |
| **Élément le plus exposé** | Équipement avec le score pondéré le plus élevé | `fact_resultats_techniques` | Serveur web Alpha |
| **Couverture des chapitres DNSSI** | Nb chapitres couverts / 14 | `fact_chapitre_audit` | 14/14 = 100% |
| **Nb de clauses identifiées** | Total des codes DNSSI extraits | `fact_chapitre_audit.clauses` | 104 clauses |
| **Confiance de l'extraction** | Score global de fiabilité des données extraites | `dim_audit.confiance_extraction` | 94% |

---

## 7 — Commandes de démonstration

### Démarrer la plateforme
```powershell
cd "~/OneDrive - um5.ac.ma/Bureau/dgssi-compilance - Copie"
docker compose up -d
docker compose ps    # Vérifier : 7 services UP
```

### Lancer l'extraction d'un rapport (venv local)
```powershell
.\venv\Scripts\Activate.ps1
python scripts/extraire_audit_depuis_silver.py "Exemple de rapport d'audit.pdf"
```

### Lancer le pipeline dbt
```powershell
cd dbt_project
dbt run      # Exécute les 11 modèles
dbt test     # Exécute les 37 tests (tous doivent passer)
```

### Requêtes SQL pour la démo
```sql
-- Voir les audits chargés
SELECT audit_id, iiv_nom, taux_conformite_global, date_extraction
FROM public_marts.dim_audit;

-- Voir les équipements les plus exposés
SELECT element_audite, critique, elevee, moyenne, faible, score_exposition_pondere
FROM public_marts.fact_resultats_techniques
ORDER BY score_exposition_pondere DESC;

-- Voir les chapitres DNSSI couverts
SELECT d.code_chapitre, f.nom_chapitre, f.clauses
FROM public_marts.fact_chapitre_audit f
JOIN public_marts.dim_chapitre_dnssi d ON f.chapitre_dnssi_id = d.chapitre_dnssi_id;

-- Voir les non-conformités extraites par LLM
SELECT resume_constat, methode_extraction, confiance, a_verifier
FROM public_marts.fact_non_conformite
LIMIT 10;
```

### Accès aux interfaces
| Interface | URL | Login | Password |
|-----------|-----|-------|----------|
| **Airflow** (orchestration) | http://localhost:8085 | admin | 6g74eSxyRmfsPEX6 |
| **Grafana** (monitoring) | http://localhost:3000 | admin | dgssi_grafana |
| **MinIO** (stockage) | http://localhost:9001 | dgssi_admin | changeme123 |
| **NiFi** (ingestion) | https://localhost:8443 | admin | dgssiAdmin123! |
| **Flask** (dashboard) | http://localhost:5000 | — | — |

---

## 8 — Correspondance avec la fiche de projet

| Objectif de la fiche | ✅ Réalisé | Comment |
|---------------------|-----------|---------|
| Pipelines d'ingestion automatisée | ✅ | NiFi → MinIO (Bronze/Silver/Gold) |
| Processus ETL/ELT | ✅ | Python + dbt (11 modèles, 37 tests) |
| Data Warehouse + Data Lake | ✅ | MinIO (Lake) + PostgreSQL (Warehouse, schéma étoile) |
| Modèle de données centralisé | ✅ | 6 tables opérationnelles + 9 tables warehouse + 9 vues dbt |
| Base analytique avec croisement | ✅ | dbt marts croise audits × chapitres × exigences |
| KPIs de conformité | ✅ | Taux, écarts, couverture, exposition (voir §6) |
| Détection automatique des écarts | ✅ | Moteur de conformité Python + alertes Grafana |
| Visualisation et reporting | ✅ | Power BI + Dashboard Flask + Grafana |
| Tableaux de bord analytiques | ✅ | Dashboard Flask + Grafana PostgreSQL |
| Qualité et traçabilité | ✅ | dbt tests (37), score de confiance, `a_verifier` flag |
| Référentiel de conformité | ✅ | 14 chapitres DNSSI v2 (seed dbt) + exigences YAML |
| Moteur d'analyse de conformité | ✅ | `moteur_conformite.py` + `calculer_taux_conformite.py` |
| Orchestration | ✅ | Airflow DAG : ETL → dbt run → dbt test |
| Monitoring et alerting | ✅ | Prometheus + Grafana + 2 alertes (écarts critiques, taux < 50%) |
