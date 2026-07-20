select
    row_number() over (order by iiv_nom, iiv_secteur) as iiv_key,
    iiv_nom,
    iiv_secteur
from (
    select distinct iiv_nom, iiv_secteur
    from "dgssi"."public_staging"."stg_audits"
) as iiv_distinct