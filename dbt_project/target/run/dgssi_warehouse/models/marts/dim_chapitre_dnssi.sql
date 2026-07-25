
  
    

  create  table "dgssi"."public_marts"."dim_chapitre_dnssi__dbt_tmp"
  
  
    as
  
  (
    -- dim_chapitre_dnssi.sql
-- Dimension FIXE des 14 chapitres du référentiel DNSSI v2.
-- Source : seed statique `chapitres_dnssi_ref.csv` — ne dépend d'aucun audit.
-- Contient exactement 14 lignes, une par chapitre réglementaire.

select
    chapitre_dnssi_id,
    code_chapitre,
    nom_chapitre,
    domaine
from "dgssi"."public_marts"."chapitres_dnssi_ref"
  );
  