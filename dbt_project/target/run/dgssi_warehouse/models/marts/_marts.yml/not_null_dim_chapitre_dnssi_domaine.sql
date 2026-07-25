
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select domaine
from "dgssi"."public_marts"."dim_chapitre_dnssi"
where domaine is null



  
  
      
    ) dbt_internal_test