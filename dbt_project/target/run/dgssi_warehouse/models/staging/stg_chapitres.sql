
  create view "dgssi"."public_staging"."stg_chapitres__dbt_tmp"
    
    
  as (
    select
    id as chapitre_id,
    audit_id,
    nom_chapitre,
    clauses
from "dgssi"."public"."chapitres"
  );