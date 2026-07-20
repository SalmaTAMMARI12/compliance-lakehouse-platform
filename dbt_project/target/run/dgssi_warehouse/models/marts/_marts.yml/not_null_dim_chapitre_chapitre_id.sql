
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select chapitre_id
from "dgssi"."public_marts"."dim_chapitre"
where chapitre_id is null



  
  
      
    ) dbt_internal_test