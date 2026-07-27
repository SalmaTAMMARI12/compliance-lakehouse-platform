026-07-25, 17:04:57 UTC] {local_task_job_runner.py:123} ▶ Pre task execution logs
[2026-07-25, 17:04:57 UTC] {subprocess.py:78} INFO - Tmp dir root location: /tmp
[2026-07-25, 17:04:57 UTC] {subprocess.py:88} INFO - Running command: ['/usr/bin/bash', '-c', 'cd /opt/airflow/project/dbt_project && POSTGRES_HOST=dgssi-postgres POSTGRES_PORT=5432 POSTGRES_DB=$POSTGRES_DB POSTGRES_USER=$POSTGRES_USER POSTGRES_PASSWORD=$POSTGRES_PASSWORD MINIO_ENDPOINT=dgssi-minio:9000 MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY MINIO_SECRET_KEY=$MINIO_SECRET_KEY  dbt test --profiles-dir /opt/airflow/project/dbt_project --project-dir /opt/airflow/project/dbt_project']
[2026-07-25, 17:04:57 UTC] {subprocess.py:99} INFO - Output:
[2026-07-25, 17:05:00 UTC] {subprocess.py:106} INFO - 17:05:00  Running with dbt=1.12.0
[2026-07-25, 17:05:01 UTC] {subprocess.py:106} INFO - 17:05:01  Registered adapter: postgres=1.11.0
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  Found 13 models, 1 seed, 65 data tests, 6 sources, 593 macros
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  Concurrency: 4 threads (target='dev')
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  1 of 65 START test accepted_values_fact_conformite_statut__Conforme__Non_conforme__Partiellement_conforme  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  2 of 65 START test dbt_utils_accepted_range_dim_audit_taux_conformite_global__True__100__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  3 of 65 START test dbt_utils_accepted_range_fact_conformite_nb_ecarts_critiques__True__9999__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  4 of 65 START test dbt_utils_accepted_range_fact_conformite_taux_conformite_global__True__100__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  1 of 65 FAIL 1 accepted_values_fact_conformite_statut__Conforme__Non_conforme__Partiellement_conforme  [FAIL 1 in 0.27s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  4 of 65 PASS dbt_utils_accepted_range_fact_conformite_taux_conformite_global__True__100__0  [PASS in 0.27s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  3 of 65 PASS dbt_utils_accepted_range_fact_conformite_nb_ecarts_critiques__True__9999__0  [PASS in 0.27s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  2 of 65 PASS dbt_utils_accepted_range_dim_audit_taux_conformite_global__True__100__0  [PASS in 0.28s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  5 of 65 START test dbt_utils_accepted_range_fact_non_conformite_confiance__True__1__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  6 of 65 START test dbt_utils_accepted_range_fact_resultats_techniques_critique__True__9999__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  7 of 65 START test dbt_utils_accepted_range_fact_resultats_techniques_elevee__True__9999__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  8 of 65 START test dbt_utils_accepted_range_fact_resultats_techniques_faible__True__9999__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  7 of 65 PASS dbt_utils_accepted_range_fact_resultats_techniques_elevee__True__9999__0  [PASS in 0.15s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  8 of 65 PASS dbt_utils_accepted_range_fact_resultats_techniques_faible__True__9999__0  [PASS in 0.15s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  6 of 65 PASS dbt_utils_accepted_range_fact_resultats_techniques_critique__True__9999__0  [PASS in 0.16s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  5 of 65 PASS dbt_utils_accepted_range_fact_non_conformite_confiance__True__1__0  [PASS in 0.17s]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  9 of 65 START test dbt_utils_accepted_range_fact_resultats_techniques_moyenne__True__9999__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  10 of 65 START test dbt_utils_accepted_range_fact_resultats_techniques_score_exposition_pondere__True__999999__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  11 of 65 START test dbt_utils_accepted_range_fact_resultats_techniques_score_exposition_total__True__99999__0  [RUN]
[2026-07-25, 17:05:03 UTC] {subprocess.py:106} INFO - 17:05:03  12 of 65 START test not_null_dim_audit_audit_id ................................ [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  9 of 65 PASS dbt_utils_accepted_range_fact_resultats_techniques_moyenne__True__9999__0  [PASS in 0.14s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  10 of 65 PASS dbt_utils_accepted_range_fact_resultats_techniques_score_exposition_pondere__True__999999__0  [PASS in 0.16s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  12 of 65 PASS not_null_dim_audit_audit_id ...................................... [PASS in 0.15s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  11 of 65 PASS dbt_utils_accepted_range_fact_resultats_techniques_score_exposition_total__True__99999__0  [PASS in 0.16s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  13 of 65 START test not_null_dim_audit_iiv_key ................................. [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  14 of 65 START test not_null_dim_chapitre_dnssi_chapitre_dnssi_id .............. [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  15 of 65 START test not_null_dim_chapitre_dnssi_code_chapitre .................. [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  16 of 65 START test not_null_dim_chapitre_dnssi_domaine ........................ [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  13 of 65 PASS not_null_dim_audit_iiv_key ....................................... [PASS in 0.15s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  16 of 65 PASS not_null_dim_chapitre_dnssi_domaine .............................. [PASS in 0.15s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  17 of 65 START test not_null_dim_chapitre_dnssi_nom_chapitre ................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  14 of 65 PASS not_null_dim_chapitre_dnssi_chapitre_dnssi_id .................... [PASS in 0.17s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  15 of 65 PASS not_null_dim_chapitre_dnssi_code_chapitre ........................ [PASS in 0.17s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  18 of 65 START test not_null_dim_iiv_iiv_key ................................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  19 of 65 START test not_null_dim_iiv_iiv_nom ................................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  20 of 65 START test not_null_dim_iiv_iiv_secteur ............................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  17 of 65 PASS not_null_dim_chapitre_dnssi_nom_chapitre ......................... [PASS in 0.18s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  18 of 65 PASS not_null_dim_iiv_iiv_key ......................................... [PASS in 0.16s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  20 of 65 PASS not_null_dim_iiv_iiv_secteur ..................................... [PASS in 0.16s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  21 of 65 START test not_null_fact_chapitre_audit_audit_id ...................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  19 of 65 PASS not_null_dim_iiv_iiv_nom ......................................... [PASS in 0.18s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  22 of 65 START test not_null_fact_chapitre_audit_chapitre_audit_id ............. [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  23 of 65 START test not_null_fact_chapitre_audit_nom_chapitre .................. [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  24 of 65 START test not_null_fact_conformite_audit_id .......................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  22 of 65 PASS not_null_fact_chapitre_audit_chapitre_audit_id ................... [PASS in 0.15s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  21 of 65 PASS not_null_fact_chapitre_audit_audit_id ............................ [PASS in 0.17s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  23 of 65 PASS not_null_fact_chapitre_audit_nom_chapitre ........................ [PASS in 0.15s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  25 of 65 START test not_null_fact_conformite_evaluation_id ..................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  26 of 65 START test not_null_fact_non_conformite_audit_id ...................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  24 of 65 PASS not_null_fact_conformite_audit_id ................................ [PASS in 0.15s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  27 of 65 START test not_null_fact_non_conformite_chapitre_id ................... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  28 of 65 START test not_null_fact_non_conformite_non_conformite_id ............. [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  25 of 65 PASS not_null_fact_conformite_evaluation_id ........................... [PASS in 0.16s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  29 of 65 START test not_null_fact_resultats_techniques_audit_id ................ [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  27 of 65 PASS not_null_fact_non_conformite_chapitre_id ......................... [PASS in 0.16s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  26 of 65 PASS not_null_fact_non_conformite_audit_id ............................ [PASS in 0.18s]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  30 of 65 START test not_null_fact_resultats_techniques_element_audite .......... [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  31 of 65 START test not_null_fact_resultats_techniques_resultat_id ............. [RUN]
[2026-07-25, 17:05:04 UTC] {subprocess.py:106} INFO - 17:05:04  28 of 65 PASS not_null_fact_non_conformite_non_conformite_id ................... [PASS in 0.16s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  32 of 65 START test not_null_stg_audits_audit_id ............................... [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  29 of 65 PASS not_null_fact_resultats_techniques_audit_id ...................... [PASS in 0.17s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  33 of 65 START test not_null_stg_chapitres_audit_id ............................ [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  31 of 65 PASS not_null_fact_resultats_techniques_resultat_id ................... [PASS in 0.15s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  30 of 65 PASS not_null_fact_resultats_techniques_element_audite ................ [PASS in 0.16s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  34 of 65 START test not_null_stg_chapitres_chapitre_id ......................... [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  32 of 65 PASS not_null_stg_audits_audit_id ..................................... [PASS in 0.15s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  35 of 65 START test not_null_stg_evaluations_conformite_audit_id ............... [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  36 of 65 START test not_null_stg_evaluations_conformite_evaluation_id .......... [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  33 of 65 PASS not_null_stg_chapitres_audit_id .................................. [PASS in 0.17s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  37 of 65 START test not_null_stg_historique_versions_audit_id .................. [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  35 of 65 PASS not_null_stg_evaluations_conformite_audit_id ..................... [PASS in 0.15s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  34 of 65 PASS not_null_stg_chapitres_chapitre_id ............................... [PASS in 0.15s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  36 of 65 PASS not_null_stg_evaluations_conformite_evaluation_id ................ [PASS in 0.12s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  38 of 65 START test not_null_stg_historique_versions_historique_id ............. [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  39 of 65 START test not_null_stg_non_conformites_chapitre_id ................... [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  40 of 65 START test not_null_stg_non_conformites_non_conformite_id ............. [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  37 of 65 PASS not_null_stg_historique_versions_audit_id ........................ [PASS in 0.14s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  39 of 65 PASS not_null_stg_non_conformites_chapitre_id ......................... [PASS in 0.13s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  41 of 65 START test not_null_stg_resultats_techniques_audit_id ................. [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  38 of 65 PASS not_null_stg_historique_versions_historique_id ................... [PASS in 0.14s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  42 of 65 START test not_null_stg_resultats_techniques_resultat_id .............. [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  43 of 65 START test relationships_dim_audit_iiv_key__iiv_key__ref_dim_iiv_ ..... [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  40 of 65 PASS not_null_stg_non_conformites_non_conformite_id ................... [PASS in 0.16s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  44 of 65 START test relationships_fact_chapitre_audit_audit_id__audit_id__ref_dim_audit_  [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  41 of 65 PASS not_null_stg_resultats_techniques_audit_id ....................... [PASS in 0.17s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  45 of 65 START test relationships_fact_conformite_audit_id__audit_id__ref_dim_audit_  [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  42 of 65 PASS not_null_stg_resultats_techniques_resultat_id .................... [PASS in 0.17s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  43 of 65 PASS relationships_dim_audit_iiv_key__iiv_key__ref_dim_iiv_ ........... [PASS in 0.18s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  46 of 65 START test relationships_fact_non_conformite_chapitre_id__chapitre_audit_id__ref_fact_chapitre_audit_  [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  47 of 65 START test relationships_stg_chapitres_audit_id__audit_id__ref_stg_audits_  [RUN]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  44 of 65 PASS relationships_fact_chapitre_audit_audit_id__audit_id__ref_dim_audit_  [PASS in 0.17s]
[2026-07-25, 17:05:05 UTC] {subprocess.py:106} INFO - 17:05:05  48 of 65 START test relationships_stg_evaluations_conformite_audit_id__audit_id__ref_stg_audits_  [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  45 of 65 PASS relationships_fact_conformite_audit_id__audit_id__ref_dim_audit_ . [PASS in 0.33s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  46 of 65 PASS relationships_fact_non_conformite_chapitre_id__chapitre_audit_id__ref_fact_chapitre_audit_  [PASS in 0.31s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  49 of 65 START test relationships_stg_historique_versions_audit_id__audit_id__ref_stg_audits_  [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  47 of 65 PASS relationships_stg_chapitres_audit_id__audit_id__ref_stg_audits_ .. [PASS in 0.33s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  50 of 65 START test relationships_stg_non_conformites_chapitre_id__chapitre_id__ref_stg_chapitres_  [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  51 of 65 START test relationships_stg_resultats_techniques_audit_id__audit_id__ref_stg_audits_  [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  48 of 65 PASS relationships_stg_evaluations_conformite_audit_id__audit_id__ref_stg_audits_  [PASS in 0.19s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  52 of 65 START test unique_dim_audit_audit_id .................................. [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  49 of 65 PASS relationships_stg_historique_versions_audit_id__audit_id__ref_stg_audits_  [PASS in 0.19s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  50 of 65 PASS relationships_stg_non_conformites_chapitre_id__chapitre_id__ref_stg_chapitres_  [PASS in 0.17s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  53 of 65 START test unique_dim_chapitre_dnssi_chapitre_dnssi_id ................ [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  54 of 65 START test unique_dim_chapitre_dnssi_code_chapitre .................... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  51 of 65 PASS relationships_stg_resultats_techniques_audit_id__audit_id__ref_stg_audits_  [PASS in 0.16s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  52 of 65 PASS unique_dim_audit_audit_id ........................................ [PASS in 0.15s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  55 of 65 START test unique_dim_iiv_iiv_key ..................................... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  56 of 65 START test unique_fact_chapitre_audit_chapitre_audit_id ............... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  53 of 65 PASS unique_dim_chapitre_dnssi_chapitre_dnssi_id ...................... [PASS in 0.13s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  54 of 65 PASS unique_dim_chapitre_dnssi_code_chapitre .......................... [PASS in 0.14s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  57 of 65 START test unique_fact_conformite_evaluation_id ....................... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  58 of 65 START test unique_fact_non_conformite_non_conformite_id ............... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  55 of 65 PASS unique_dim_iiv_iiv_key ........................................... [PASS in 0.15s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  56 of 65 PASS unique_fact_chapitre_audit_chapitre_audit_id ..................... [PASS in 0.15s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  59 of 65 START test unique_fact_resultats_techniques_resultat_id ............... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  60 of 65 START test unique_stg_audits_audit_id ................................. [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  57 of 65 PASS unique_fact_conformite_evaluation_id ............................. [PASS in 0.16s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  58 of 65 PASS unique_fact_non_conformite_non_conformite_id ..................... [PASS in 0.15s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  61 of 65 START test unique_stg_chapitres_chapitre_id ........................... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  62 of 65 START test unique_stg_evaluations_conformite_evaluation_id ............ [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  59 of 65 PASS unique_fact_resultats_techniques_resultat_id ..................... [PASS in 0.14s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  60 of 65 PASS unique_stg_audits_audit_id ....................................... [PASS in 0.15s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  63 of 65 START test unique_stg_historique_versions_historique_id ............... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  64 of 65 START test unique_stg_non_conformites_non_conformite_id ............... [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  61 of 65 PASS unique_stg_chapitres_chapitre_id ................................. [PASS in 0.15s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  62 of 65 PASS unique_stg_evaluations_conformite_evaluation_id .................. [PASS in 0.14s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  65 of 65 START test unique_stg_resultats_techniques_resultat_id ................ [RUN]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  63 of 65 PASS unique_stg_historique_versions_historique_id ..................... [PASS in 0.13s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  64 of 65 PASS unique_stg_non_conformites_non_conformite_id ..................... [PASS in 0.12s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  65 of 65 PASS unique_stg_resultats_techniques_resultat_id ...................... [PASS in 0.09s]
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06
[2026-07-25, 17:05:06 UTC] {subprocess.py:106} INFO - 17:05:06  Finished running 65 data tests in 0 hours 0 minutes and 3.68 seconds (3.68s).
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07  Completed with 1 error, 0 partial successes, and 0 warnings:
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07  [ERROR]: in test accepted_values_fact_conformite_statut__Conforme__Non_conforme__Partiellement_conforme (models/marts/_marts.yml)
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07    Got 1 result, configured to fail if != 0
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07    compiled code at target/compiled/dgssi_warehouse/models/marts/_marts.yml/accepted_values_fact_conformit_567db53fccf90b3ff6effe1850437e38.sql
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07
[2026-07-25, 17:05:07 UTC] {subprocess.py:106} INFO - 17:05:07  Done. PASS=64 WARN=0 ERROR=1 SKIP=0 NO-OP=0 REUSED=0 TOTAL=65
[2026-07-25, 17:05:08 UTC] {subprocess.py:110} INFO - Command exited with return code 1
[2026-07-25, 17:05:08 UTC] {taskinstance.py:3313} ERROR - Task failed with exception
Traceback (most recent call last):
File "/home/airflow/.local/lib/python3.11/site-packages/airflow/models/taskinstance.py", line 768, in _execute_task
result = _execute_callable(context=context, **execute_callable_kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/airflow/.local/lib/python3.11/site-packages/airflow/models/taskinstance.py", line 734, in _execute_callable
return ExecutionCallableRunner(
^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/airflow/.local/lib/python3.11/site-packages/airflow/utils/operator_helpers.py", line 252, in run
return self.func(*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/airflow/.local/lib/python3.11/site-packages/airflow/models/baseoperator.py", line 424, in wrapper
return func(self, *args, **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/airflow/.local/lib/python3.11/site-packages/airflow/operators/bash.py", line 276, in execute
raise AirflowException(
airflow.exceptions.AirflowException: Bash command failed. The command returned a non-zero exit code 1.
[2026-07-25, 17:05:08 UTC] {taskinstance.py:1226} INFO - Marking task as FAILED. dag_id=pipeline_conformite_dnssi, task_id=dbt_test, run_id=manual__2026-07-25T17:04:24.936383+00:00, execution_date=20260725T170424, start_date=20260725T170457, end_date=20260725T170508
[2026-07-25, 17:05:08 UTC] {taskinstance.py:341} ▶ Post task execution logsFROM apache/airflow:2.10.5-python3.11

# ── Dépendances système ──────────────────────────────────
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    git \
    && rm -rf /var/lib/apt/lists/*
USER airflow

# ── Dépendances Python ───────────────────────────────────
# NOTE : PAS de sqlalchemy>=2.0 ici !
# Airflow fournit déjà SQLAlchemy 1.4.x en interne.
# Les scripts ETL (etl_vers_warehouse.py) utilisent psycopg2 directement.
# L'extraction Docling (qui nécessite SQLAlchemy 2.x) tourne en local, hors Airflow.
RUN pip install --no-cache-dir --timeout 300 \
    psycopg2-binary \
    minio \
    boto3 \
    pyyaml \
    python-dotenv \
    pydantic \
    pydantic-settings \
    "dbt-core>=1.8.0,<2.0.0" \
    "dbt-postgres>=1.8.0,<2.0.0"
