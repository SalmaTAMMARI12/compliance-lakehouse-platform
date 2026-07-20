
    
    

select
    evaluation_id as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."fact_conformite"
where evaluation_id is not null
group by evaluation_id
having count(*) > 1


