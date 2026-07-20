
  
    

  create  table "dgssi"."public_marts"."dim_chapitre__dbt_tmp"
  
  
    as
  
  (
    select
    chapitre_id,
    audit_id,
    nom_chapitre,
    clauses
from "dgssi"."public_staging"."stg_chapitres"
  );
  