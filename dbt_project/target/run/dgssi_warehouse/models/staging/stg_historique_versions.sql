
  create view "dgssi"."public_staging"."stg_historique_versions__dbt_tmp"
    
    
  as (
    select
    id as historique_id,
    audit_id,
    version,
    date as date_version,
    commentaire
from "dgssi"."public"."historique_versions"
  );