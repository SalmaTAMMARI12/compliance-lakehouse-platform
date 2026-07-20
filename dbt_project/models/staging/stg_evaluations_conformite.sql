select
    id as evaluation_id,
    audit_id,
    statut,
    seuil_applique,
    nb_ecarts_critiques,
    element_le_plus_expose,
    date_evaluation
from {{ source('dgssi', 'evaluations_conformite') }}