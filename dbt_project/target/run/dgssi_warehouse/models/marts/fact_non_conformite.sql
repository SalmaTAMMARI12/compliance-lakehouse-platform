
  
    

  create  table "dgssi"."public_marts"."fact_non_conformite__dbt_tmp"
  
  
    as
  
  (
    select
    nc.non_conformite_id,
    nc.chapitre_id,
    c.audit_id,
    nc.texte_source,
    nc.resume_constat,
    nc.recommandation,
    nc.actifs_concernes,
    nc.echeance,
    nc.confiance,
    nc.methode_extraction,
    nc.a_verifier
from "dgssi"."public_staging"."stg_non_conformites" nc
left join "dgssi"."public_staging"."stg_chapitres" c
    on nc.chapitre_id = c.chapitre_id
  );
  