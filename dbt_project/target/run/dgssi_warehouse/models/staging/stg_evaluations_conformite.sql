
  create view "dgssi"."public_staging"."stg_evaluations_conformite__dbt_tmp"
    
    
  as (
    select
    id as evaluation_id,
    audit_id,
    statut,
    seuil_applique,
    nb_ecarts_critiques,
    element_le_plus_expose,
    date_evaluation
from "dgssi"."public"."evaluations_conformite"
  );