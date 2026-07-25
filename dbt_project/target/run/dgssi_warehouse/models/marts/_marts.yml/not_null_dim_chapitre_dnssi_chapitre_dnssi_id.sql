
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select chapitre_dnssi_id
from "dgssi"."public_marts"."dim_chapitre_dnssi"
where chapitre_dnssi_id is null



  
  
      
    ) dbt_internal_test