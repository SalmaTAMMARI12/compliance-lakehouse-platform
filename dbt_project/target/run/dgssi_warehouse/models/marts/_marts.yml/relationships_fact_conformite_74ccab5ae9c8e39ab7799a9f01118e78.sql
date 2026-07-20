
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select audit_id as from_field
    from "dgssi"."public_marts"."fact_conformite"
    where audit_id is not null
),

parent as (
    select audit_id as to_field
    from "dgssi"."public_marts"."dim_audit"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test