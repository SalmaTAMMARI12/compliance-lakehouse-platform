
    
    

with child as (
    select chapitre_id as from_field
    from "dgssi"."public_staging"."stg_non_conformites"
    where chapitre_id is not null
),

parent as (
    select chapitre_id as to_field
    from "dgssi"."public_staging"."stg_chapitres"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


