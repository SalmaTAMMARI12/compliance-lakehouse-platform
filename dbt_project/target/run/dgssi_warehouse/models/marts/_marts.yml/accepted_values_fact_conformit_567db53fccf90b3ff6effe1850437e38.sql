
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

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
    'Conforme','Non conforme','Partiellement conforme'
)



  
  
      
    ) dbt_internal_test