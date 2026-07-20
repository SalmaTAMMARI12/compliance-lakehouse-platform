
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select historique_id
from "dgssi"."public_staging"."stg_historique_versions"
where historique_id is null



  
  
      
    ) dbt_internal_test