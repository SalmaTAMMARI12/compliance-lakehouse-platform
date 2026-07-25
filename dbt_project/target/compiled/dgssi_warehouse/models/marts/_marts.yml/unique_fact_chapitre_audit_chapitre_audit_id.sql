
    
    

select
    chapitre_audit_id as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."fact_chapitre_audit"
where chapitre_audit_id is not null
group by chapitre_audit_id
having count(*) > 1


