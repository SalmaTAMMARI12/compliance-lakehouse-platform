-- fact_chapitre_audit.sql
-- Table de faits : occurrences de chapitres DNSSI constatées dans chaque audit.
-- Une ligne = un chapitre évalué dans un audit donné.
-- Lien vers dim_chapitre_dnssi via correspondance sur nom_chapitre.
-- Lien vers dim_audit via audit_id.

select
    c.chapitre_id                   as chapitre_audit_id,
    c.audit_id,
    d.chapitre_dnssi_id,
    d.code_chapitre,
    c.nom_chapitre,
    c.clauses
from {{ ref('stg_chapitres') }} c
left join {{ ref('dim_chapitre_dnssi') }} d
    on lower(trim(c.nom_chapitre)) = lower(trim(d.nom_chapitre))
