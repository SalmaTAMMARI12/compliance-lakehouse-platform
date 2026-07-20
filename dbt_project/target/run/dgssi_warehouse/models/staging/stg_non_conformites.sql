
  create view "dgssi"."public_staging"."stg_non_conformites__dbt_tmp"
    
    
  as (
    select
    id as non_conformite_id,
    chapitre_id,
    texte_source,
    resume_constat,
    recommandation,
    actifs_concernes,
    echeance,
    confiance,
    methode_extraction,
    a_verifier
from "dgssi"."public"."non_conformites"
  );