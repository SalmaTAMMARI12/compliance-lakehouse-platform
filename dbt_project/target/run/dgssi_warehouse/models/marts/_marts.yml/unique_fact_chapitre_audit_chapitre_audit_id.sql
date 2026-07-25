
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    chapitre_audit_id as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."fact_chapitre_audit"
where chapitre_audit_id is not null
group by chapitre_audit_id
having count(*) > 1



  
  
      
    ) dbt_internal_test