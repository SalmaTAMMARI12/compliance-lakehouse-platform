
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select resultat_id
from "dgssi"."public_marts"."fact_resultats_techniques"
where resultat_id is null



  
  
      
    ) dbt_internal_test