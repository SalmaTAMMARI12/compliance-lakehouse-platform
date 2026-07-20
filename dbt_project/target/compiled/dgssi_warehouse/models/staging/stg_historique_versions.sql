select
    id as historique_id,
    audit_id,
    version,
    date as date_version,
    commentaire
from "dgssi"."public"."historique_versions"