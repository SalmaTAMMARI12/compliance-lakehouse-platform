
    
    

with all_values as (

    select
        statut as value_field,
        count(*) as n_records

    from "dgssi"."public_marts"."fact_conformite"
    group by statut

)

select *
from all_values
where value_field not in (
    'CONFORME','NON_CONFORME','SOUS_RESERVES'
)


