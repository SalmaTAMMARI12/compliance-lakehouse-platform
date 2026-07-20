
  create view "dgssi"."public_staging"."stg_audits__dbt_tmp"
    
    
  as (
    -- Nettoyage/renommage de la table source `audits`. Pas de logique métier ici.
select
    id as audit_id,
    iiv_nom,
    iiv_secteur,
    prestataire_audit,
    classification,
    taux_conformite_global,
    date_extraction,
    confiance_extraction,
    confiance_par_categorie,
    chemin_gold
from "dgssi"."public"."audits"
  );