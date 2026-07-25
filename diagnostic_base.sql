-- ============================================================
-- DIAGNOSTIC BASE DGSSI — à exécuter avec psql ou un client SQL
--   psql -h localhost -U dgssi -d dgssi -f diagnostic_base.sql
-- Chaque requête est commentée avec ce qu'il FAUT observer.
-- ============================================================


-- 1. Combien d'audits en base ? --------------------------------
-- Attendu : au moins 1 ligne. Si 0 -> le pipeline n'a jamais
-- écrit en base, rien d'autre à vérifier tant que ça n'est pas réglé.
SELECT id, iiv_nom, prestataire_audit, classification,
       taux_conformite_global, date_extraction, confiance_extraction
FROM audits
ORDER BY id DESC;


-- 2. Y a-t-il bien 14 chapitres pour l'audit le plus récent ? --
-- Attendu : exactement 14 lignes (§3.1 à §3.14 du rapport DNSSI).
-- Si < 14 -> extracteur_clauses.py n'a pas tout capturé.
-- Si > 14 -> doublons, à investiguer (probablement un audit rejoué
-- deux fois sans déduplication correcte dans audit_repository.py).
SELECT count(*) AS nb_chapitres
FROM chapitres
WHERE audit_id = (SELECT max(id) FROM audits);


-- 3. Liste des chapitres avec leur nombre de clauses -----------
-- Attendu : chaque chapitre a >0 clauses (voir dnssi_v2.yaml pour
-- le nombre exact attendu par chapitre, ex. Cryptographie = 2,
-- Sécurité liée à l'exploitation = 19).
SELECT nom_chapitre, json_array_length(clauses::json) AS nb_clauses
FROM chapitres
WHERE audit_id = (SELECT max(id) FROM audits)
ORDER BY id;


-- 4. LE TEST CRITIQUE — chapitres "Conforme, aucun écart" ------
-- qui auraient QUAND MÊME des non-conformités en base.
-- Attendu : 0 ligne. Si ce test retourne des lignes, c'est le bug
-- qu'on cherchait : un chapitre marqué conforme dans le rapport
-- source a quand même généré un faux écart.
-- ⚠ Les noms ci-dessous sont ceux identifiés comme "Conforme.
-- Aucun écart relevé." dans le rapport de référence (§3.2, §3.3,
-- §3.7) — adapte la liste si ton rapport diffère.
SELECT c.nom_chapitre, nc.id AS non_conformite_id, nc.resume_constat,
       nc.methode_extraction, nc.a_verifier
FROM chapitres c
JOIN non_conformites nc ON nc.chapitre_id = c.id
WHERE c.audit_id = (SELECT max(id) FROM audits)
  AND c.nom_chapitre IN (
      'Organisation de la sécurité',
      'Sécurité des ressources humaines',
      'Sécurité physique'
  );


-- 5. Répartition des non-conformités par chapitre ---------------
-- Attendu : total cohérent avec le nombre de constats visibles
-- dans le rapport pour chaque chapitre (compare visuellement avec
-- le PDF). Chapitres listés en 4. doivent apparaître à 0 ici.
SELECT c.nom_chapitre, count(nc.id) AS nb_ecarts
FROM chapitres c
LEFT JOIN non_conformites nc ON nc.chapitre_id = c.id
WHERE c.audit_id = (SELECT max(id) FROM audits)
GROUP BY c.nom_chapitre, c.id
ORDER BY nb_ecarts DESC;


-- 6. Total des non-conformités vs total attendu du rapport ------
-- Attendu (rapport de référence) : 19 (11 significatifs +
-- 7 non-significatifs + 1 remarque, page 10-11). Ce total agrégé
-- N'EST PAS encore stocké en base (voir §2 de ma réponse précédente)
-- donc compare ici au chiffre lu manuellement dans le PDF.
SELECT count(*) AS total_non_conformites
FROM non_conformites nc
JOIN chapitres c ON c.id = nc.chapitre_id
WHERE c.audit_id = (SELECT max(id) FROM audits);


-- 7. Qualité des champs enrichis par le LLM ----------------------
-- Regarde la proportion :
--   - resume_constat non vide -> devrait être ~100%
--   - recommandation non vide -> normal que ce soit partiel
--     (seulement quand le texte source mentionne une action)
--   - actifs_concernes non vide -> normal que ce soit partiel
--   - confiance moyenne -> doit être cohérente (pas de 0.0 en masse,
--     signe d'échecs LLM silencieux)
SELECT
    count(*) AS total,
    count(*) FILTER (WHERE resume_constat IS NOT NULL AND resume_constat <> '') AS avec_resume,
    count(*) FILTER (WHERE recommandation IS NOT NULL AND recommandation <> '') AS avec_recommandation,
    count(*) FILTER (WHERE actifs_concernes::text NOT IN ('[]', 'null')) AS avec_actifs,
    count(*) FILTER (WHERE echeance IS NOT NULL) AS avec_echeance,
    round(avg(confiance)::numeric, 2) AS confiance_moyenne,
    count(*) FILTER (WHERE confiance = 0.0) AS nb_echecs_llm,
    count(*) FILTER (WHERE a_verifier = true) AS nb_a_verifier
FROM non_conformites nc
JOIN chapitres c ON c.id = nc.chapitre_id
WHERE c.audit_id = (SELECT max(id) FROM audits);


-- 8. Résultats techniques (vulnérabilités par équipement) --------
-- Attendu (rapport de référence, tableau §4.5.a) : 7 équipements
-- (Architecture, Firewall Central Forcepoint, Firewall Partenaire,
-- Firewall Frontal, Switch fédérateur, Serveur de messagerie,
-- Serveur web Alpha) avec des totaux non-nuls.
SELECT element_audite, critique, elevee, moyenne, faible
FROM resultats_techniques
WHERE audit_id = (SELECT max(id) FROM audits)
ORDER BY (critique*4 + elevee*3 + moyenne*2 + faible) DESC;


-- 9. Historique des versions -------------------------------------
-- Attendu (rapport de référence) : 3 lignes (V1.0, V1.1, V 1.2).
SELECT version, date, commentaire
FROM historique_versions
WHERE audit_id = (SELECT max(id) FROM audits)
ORDER BY date;


-- 10. Cohérence référentielle générale -----------------------------
-- Attendu : 0 ligne pour chacune (pas d'orphelins).
SELECT 'chapitres sans audit' AS probleme, count(*) FROM chapitres c
    LEFT JOIN audits a ON a.id = c.audit_id WHERE a.id IS NULL
UNION ALL
SELECT 'non_conformites sans chapitre', count(*) FROM non_conformites nc
    LEFT JOIN chapitres c ON c.id = nc.chapitre_id WHERE c.id IS NULL
UNION ALL
SELECT 'resultats_techniques sans audit', count(*) FROM resultats_techniques rt
    LEFT JOIN audits a ON a.id = rt.audit_id WHERE a.id IS NULL;