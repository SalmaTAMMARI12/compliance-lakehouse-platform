
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select nom_chapitre
from "dgssi"."public_marts"."fact_chapitre_audit"
where nom_chapitre is null



  
  
      
    ) dbt_internal_test