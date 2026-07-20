select
    chapitre_id,
    audit_id,
    nom_chapitre,
    clauses
from {{ ref('stg_chapitres') }}