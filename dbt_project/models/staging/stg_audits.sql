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
    hash_sha256 || '.json' as chemin_gold,
    nb_ecarts_par_type,
    perimetres ->> 'Périmètre Fonctionnel' as perimetre_fonctionnel,
    perimetres ->> 'Périmètre Technique' as perimetre_technique
from {{ source('dgssi', 'audits') }}