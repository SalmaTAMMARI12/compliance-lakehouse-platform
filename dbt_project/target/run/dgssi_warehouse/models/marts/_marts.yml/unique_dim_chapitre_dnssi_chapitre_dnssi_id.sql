
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    chapitre_dnssi_id as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."dim_chapitre_dnssi"
where chapitre_dnssi_id is not null
group by chapitre_dnssi_id
having count(*) > 1



  
  
      
    ) dbt_internal_test