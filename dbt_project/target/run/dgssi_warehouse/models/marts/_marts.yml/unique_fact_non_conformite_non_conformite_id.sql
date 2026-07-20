
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    non_conformite_id as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."fact_non_conformite"
where non_conformite_id is not null
group by non_conformite_id
having count(*) > 1



  
  
      
    ) dbt_internal_test