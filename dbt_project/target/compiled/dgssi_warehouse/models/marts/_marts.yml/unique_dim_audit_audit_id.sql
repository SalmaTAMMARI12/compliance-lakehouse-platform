
    
    

select
    audit_id as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."dim_audit"
where audit_id is not null
group by audit_id
having count(*) > 1


