
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select iiv_key
from "dgssi"."public_marts"."dim_audit"
where iiv_key is null



  
  
      
    ) dbt_internal_test