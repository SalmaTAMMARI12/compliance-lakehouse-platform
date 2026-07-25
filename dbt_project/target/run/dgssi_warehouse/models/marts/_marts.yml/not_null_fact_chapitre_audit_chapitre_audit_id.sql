
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select chapitre_audit_id
from "dgssi"."public_marts"."fact_chapitre_audit"
where chapitre_audit_id is null



  
  
      
    ) dbt_internal_test