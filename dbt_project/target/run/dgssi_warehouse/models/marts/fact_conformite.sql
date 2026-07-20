
  
    

  create  table "dgssi"."public_marts"."fact_conformite__dbt_tmp"
  
  
    as
  
  (
    select
    e.evaluation_id,
    e.audit_id,
    e.statut,
    e.seuil_applique,
    e.nb_ecarts_critiques,
    e.element_le_plus_expose,
    e.date_evaluation,
    a.taux_conformite_global
from "dgssi"."public_staging"."stg_evaluations_conformite" e
left join "dgssi"."public_staging"."stg_audits" a
    on e.audit_id = a.audit_id
  );
  