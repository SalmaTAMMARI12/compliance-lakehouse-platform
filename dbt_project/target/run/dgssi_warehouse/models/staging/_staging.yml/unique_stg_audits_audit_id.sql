
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    audit_id as unique_field,
    count(*) as n_records

from "dgssi"."public_staging"."stg_audits"
where audit_id is not null
group by audit_id
having count(*) > 1



  
  
      
    ) dbt_internal_test