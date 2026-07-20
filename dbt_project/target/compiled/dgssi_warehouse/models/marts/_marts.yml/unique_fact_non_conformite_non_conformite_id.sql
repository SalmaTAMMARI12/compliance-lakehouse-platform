
    
    

select
    non_conformite_id as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."fact_non_conformite"
where non_conformite_id is not null
group by non_conformite_id
having count(*) > 1


