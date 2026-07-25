
    
    

select
    code_chapitre as unique_field,
    count(*) as n_records

from "dgssi"."public_marts"."dim_chapitre_dnssi"
where code_chapitre is not null
group by code_chapitre
having count(*) > 1


