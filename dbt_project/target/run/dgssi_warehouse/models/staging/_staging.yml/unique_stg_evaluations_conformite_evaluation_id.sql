
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    evaluation_id as unique_field,
    count(*) as n_records

from "dgssi"."public_staging"."stg_evaluations_conformite"
where evaluation_id is not null
group by evaluation_id
having count(*) > 1



  
  
      
    ) dbt_internal_test