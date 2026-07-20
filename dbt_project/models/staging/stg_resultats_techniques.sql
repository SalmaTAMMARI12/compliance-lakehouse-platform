select
    id as resultat_id,
    audit_id,
    element_audite,
    critique,
    elevee,
    moyenne,
    faible
from {{ source('dgssi', 'resultats_techniques') }}