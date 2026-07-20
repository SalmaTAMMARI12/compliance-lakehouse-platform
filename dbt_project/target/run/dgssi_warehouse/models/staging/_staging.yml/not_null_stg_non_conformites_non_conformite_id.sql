
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select non_conformite_id
from "dgssi"."public_staging"."stg_non_conformites"
where non_conformite_id is null



  
  
      
    ) dbt_internal_test