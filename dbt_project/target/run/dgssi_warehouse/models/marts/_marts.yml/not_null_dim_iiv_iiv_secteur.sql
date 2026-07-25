
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select iiv_secteur
from "dgssi"."public_marts"."dim_iiv"
where iiv_secteur is null



  
  
      
    ) dbt_internal_test