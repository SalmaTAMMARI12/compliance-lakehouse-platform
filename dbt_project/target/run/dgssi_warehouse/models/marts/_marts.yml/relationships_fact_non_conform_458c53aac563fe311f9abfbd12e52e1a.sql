
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select chapitre_id as from_field
    from "dgssi"."public_marts"."fact_non_conformite"
    where chapitre_id is not null
),

parent as (
    select chapitre_id as to_field
    from "dgssi"."public_marts"."dim_chapitre"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test