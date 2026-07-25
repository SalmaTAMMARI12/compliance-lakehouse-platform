
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select element_audite
from "dgssi"."public_marts"."fact_resultats_techniques"
where element_audite is null



  
  
      
    ) dbt_internal_test