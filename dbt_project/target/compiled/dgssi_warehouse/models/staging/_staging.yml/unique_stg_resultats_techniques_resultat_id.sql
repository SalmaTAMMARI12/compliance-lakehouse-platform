
    
    

select
    resultat_id as unique_field,
    count(*) as n_records

from "dgssi"."public_staging"."stg_resultats_techniques"
where resultat_id is not null
group by resultat_id
having count(*) > 1


