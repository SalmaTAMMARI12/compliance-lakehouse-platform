
  
    

  create  table "dgssi"."public_marts"."fact_resultats_techniques__dbt_tmp"
  
  
    as
  
  (
    -- fact_resultats_techniques.sql
-- Table de faits : scores d'exposition technique par équipement audité.
-- Une ligne = un élément technique audité (serveur, firewall, switch…) dans un audit.
-- score_exposition_total = somme de toutes les vulnérabilités détectées.

select
    r.resultat_id,
    r.audit_id,
    a.iiv_key,
    r.element_audite,
    coalesce(r.critique, 0)                                              as critique,
    coalesce(r.elevee, 0)                                               as elevee,
    coalesce(r.moyenne, 0)                                              as moyenne,
    coalesce(r.faible, 0)                                               as faible,
    coalesce(r.critique, 0)
        + coalesce(r.elevee, 0)
        + coalesce(r.moyenne, 0)
        + coalesce(r.faible, 0)                                         as score_exposition_total,
    -- Score pondéré : critique×4, élevée×3, moyenne×2, faible×1
    (coalesce(r.critique, 0) * 4)
        + (coalesce(r.elevee, 0) * 3)
        + (coalesce(r.moyenne, 0) * 2)
        + (coalesce(r.faible, 0) * 1)                                   as score_exposition_pondere
from "dgssi"."public_staging"."stg_resultats_techniques" r
left join "dgssi"."public_marts"."dim_audit" a
    on r.audit_id = a.audit_id
  );
  