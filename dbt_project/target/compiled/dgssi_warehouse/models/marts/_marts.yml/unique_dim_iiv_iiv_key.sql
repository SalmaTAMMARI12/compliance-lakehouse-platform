
    
    

select
    iiv_key as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."dim_iiv"
where iiv_key is not null
group by iiv_key
having count(*) > 1


