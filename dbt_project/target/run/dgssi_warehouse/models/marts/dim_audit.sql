
  
    

  create  table "dgssi"."public_marts"."dim_audit__dbt_tmp"
  
  
    as
  
  (
    select
    a.audit_id,
    iiv.iiv_key,
    a.prestataire_audit,
    a.classification,
    a.taux_conformite_global,
    a.date_extraction,
    a.confiance_extraction,
    a.confiance_par_categorie,
    a.chemin_gold
from "dgssi"."public_staging"."stg_audits" a
left join "dgssi"."public_marts"."dim_iiv" iiv
    on a.iiv_nom = iiv.iiv_nom
    and a.iiv_secteur = iiv.iiv_secteur
  );
  