select
    id as historique_id,
    audit_id,
    version,
    date as date_version,
    commentaire
from {{ source('dgssi', 'historique_versions') }}