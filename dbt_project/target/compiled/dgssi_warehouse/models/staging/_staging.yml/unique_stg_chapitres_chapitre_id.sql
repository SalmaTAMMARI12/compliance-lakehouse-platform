
    
    

select
    chapitre_id as unique_field,
    count(*) as n_records

from "dgssi"."public_staging"."stg_chapitres"
where chapitre_id is not null
group by chapitre_id
having count(*) > 1


