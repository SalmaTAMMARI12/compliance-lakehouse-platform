select
    id as chapitre_id,
    audit_id,
    nom_chapitre,
    clauses
from {{ source('dgssi', 'chapitres') }}