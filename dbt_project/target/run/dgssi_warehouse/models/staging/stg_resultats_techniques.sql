
  create view "dgssi"."public_staging"."stg_resultats_techniques__dbt_tmp"
    
    
  as (
    select
    id as resultat_id,
    audit_id,
    element_audite,
    critique,
    elevee,
    moyenne,
    faible
from "dgssi"."public"."resultats_techniques"
  );