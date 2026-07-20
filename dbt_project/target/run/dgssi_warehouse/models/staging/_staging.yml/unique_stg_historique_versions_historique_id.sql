
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    historique_id as unique_field,
    count(*) as n_records

from "dgssi"."public_staging"."stg_historique_versions"
where historique_id is not null
group by historique_id
having count(*) > 1



  
  
      
    ) dbt_internal_test