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
from {{ ref('stg_audits') }} a
left join {{ ref('dim_iiv') }} iiv
    on a.iiv_nom = iiv.iiv_nom
    and a.iiv_secteur = iiv.iiv_secteur