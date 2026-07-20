
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select evaluation_id
from "dgssi"."public_staging"."stg_evaluations_conformite"
where evaluation_id is null



  
  
      
    ) dbt_internal_test